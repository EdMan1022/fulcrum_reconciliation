import requests
from .fulcrum_variables import FulcrumVariables
from .db_variables import DbVariables
import json
import os
import pandas as pd
import datetime
import fulcrum_reconciliation.exceptions as exc
from fulcrum_reconciliation import models
from fulcrum_reconciliation.extensions import db


class AutoReconciler(object):
    """
    Wraps methods for removing bad data points from the Fulcrum completes list

    :attr list_surveys_url: (str) address for the api endpoint that returns a list of survey objects with a status
    :attribute reconcile_survey_url: (str) api endpoint that updates the completes associated with a survey
    :good_ids_list: (list) List of respondent IDs (RIDS) that are supposed to remain in the final sample
    """

    production_url = "https://api.samplicio.us/"
    sandbox_url = "https://sandbox.techops.engineering/"

    base_url = None
    list_surveys_url = None
    reconcile_survey_url = None
    good_ids_list = None
    data_check_path = "S:/Python/Data Check"
    previous_month_path = "S:/Python/Good Data by Month"
    completed_surveys = None

    callout_string = 'callout'

    def __init__(self, api_key: str, base_url: str):
        """

        :param api_key:
        """
        self.api_key = api_key
        self.base_url = base_url
        self.list_surveys_url = "{}Demand/v1/Surveys/BySurveyStatus".format(self.base_url)
        self.reconcile_survey_url = "{}Demand/v1/Surveys/Reconcile".format(self.base_url)

    def list_surveys_by_status(self, survey_status):
        """
        Queries Fulcrum API for the list of completed surveys

        :return:
        """

        request_header = {FulcrumVariables.authorization: self.api_key}
        response = requests.get("{}/{}".format(self.list_surveys_url, survey_status),
                                headers=request_header)
        response_data = response.json()
        all_surveys = response_data.get(FulcrumVariables.survey_list_name)
        return all_surveys

    def configure_reconciliation_list(self):
        """
        Sets the list of surveys to be reconciled based on the database

        :return:
        """

        # Get the list of surveys that have been completed but not reconciled
        all_surveys = models.FulcrumSurvey.query.filter_by(survey_status_code=FulcrumVariables.completed_survey_code,
                                                           reconciliation_status_code=DbVariables.not_reconciled_code).all()
        if len(all_surveys) <= 0:
            raise exc.NoCompleteSurveysError
        self.completed_surveys = all_surveys

    def reconcile_survey(self, survey: models.FulcrumSurvey):
        """
        Sends json with list of good ids for a survey to the reconciliation endpoint at the Fulcrum API

        :param survey: survey object for the survey to be reconciled
        :return:
        """

        # Check that the ids list has been set
        if self.good_ids_list is None:
            raise exc.NoGoodIDsError

        survey_number = survey.survey_number

        # Create data from ids
        request_params = {FulcrumVariables.response_ids: self.good_ids_list}
        request_data = json.dumps(request_params)

        # Create headers
        request_headers = {
            'Content-type': 'application/json',
            FulcrumVariables.authorization: self.api_key,
            'Accept': 'text/plain'
        }

        # create request url
        request_url = "{}/{}".format(self.reconcile_survey_url, survey_number)

        # send reconciliation POST
        response = requests.post(request_url, data=request_data, headers=request_headers)

        # Raise an exception if the response status code is not valid
        if response.status_code not in FulcrumVariables.reconciliation_response_code:
            raise exc.ReconciliationResponseError(response.status_code)
        survey.reconciliation_status_code = DbVariables.reconciled_code
        db.session.commit()

    def configure_month_good_ids_file(self, month, year, month_str):
        """
        Creates a list of good Fulcrum IDs from all of the data checks for a given month and year

        :param month: Integer value of the month to be compiled
        :param year: Integer value of the year
        :param month_str: Text value of month for file name
        :return:
        """

        date_list = os.listdir(self.data_check_path)
        this_month_date_str = "{}-{}".format(year, str(month).zfill(2))
        date_series = pd.Series(date_list)
        this_month_series = date_series[date_series.str.contains(this_month_date_str)]
        ids = []
        for i in this_month_series.tolist():
            try:
                data_check = pd.read_excel("{}/{}".format(self.data_check_path, i))
                good_data = data_check[data_check.loc[:, 'BadData'] != 1]
                fulcrum_data = good_data[good_data.loc[:, 'VENDOR'] == 'FU']
                ids += (fulcrum_data.loc[:, 'ID'].tolist())
            except PermissionError:
                raise exc.OpenDataFileError(i)
        pd.Series(ids).to_csv("{}/{} good data.csv".format(self.previous_month_path, month_str))

    def configure_good_ids_list(self):
        """
        Sets the good_ids_list attribute equal to the list of ids from this month and the previous month

        These ids will be sent to the reconciliation endpoint on the Fulcrum API
        :return:
        """

        date_list = os.listdir(self.data_check_path)
        today = datetime.datetime.today()
        this_month_date_str = "{}-{}".format(today.year, str(today.month).zfill(2))

        date_series = pd.Series(date_list)
        this_month_series = date_series[date_series.str.contains(this_month_date_str)]

        first_of_month = today.replace(day=1)
        last_month = first_of_month - datetime.timedelta(days=2)
        previous_month_path = "{}/{} good data.csv".format(self.previous_month_path,
                                                           datetime.datetime.strftime(last_month, '%B'))
        if not os.path.isfile(previous_month_path):
            self.configure_month_good_ids_file(last_month.month, last_month.year,
                                               datetime.datetime.strftime(last_month, '%B'))
        ids = pd.read_csv(previous_month_path, header=None).iloc[:, 1].tolist()
        for i in this_month_series.tolist():
            try:
                data_check = pd.read_excel("{}/{}".format(self.data_check_path, i))
                good_data = data_check[data_check.loc[:, 'BadData'] != 1]
                fulcrum_data = good_data[good_data.loc[:, 'VENDOR'] == 'FU']
                ids += (fulcrum_data.loc[:, 'ID'].tolist())
            except PermissionError:
                raise exc.OpenDataFileError(i)
        self.good_ids_list = ids

    def reconcile_completed_surveys(self):
        for survey in self.completed_surveys:
            self.reconcile_survey(survey)

    def reconcile_completed_callout_surveys(self):
        """
        Performs the reconciliation process for all of the surveys that contain case insensitive 'callout' in their name

        The good id list only draws from the callout data, so this needs to
        :return:
        """
        for survey in self.completed_surveys:
            if self.callout_string in survey.name.lower():
                self.reconcile_survey(survey)
