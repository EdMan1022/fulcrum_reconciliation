import requests
from .fulcrum_variables import FulcrumVariables
import json


class AutoReconciler(object):
    """
    Wraps methods for removing bad data points from the Fulcrum completes list

    :attr list_surveys_url: (str) address for the api endpoint that returns a list of survey objects with a status
    :attribute reconcile_survey_url: (str) api endpoint that updates the completes associated with a survey
    :good_ids_list: (list) List of respondent IDs (RIDS) that are supposed to remain in the final sample
    """

    base_url = "https://sandbox.techops.engineering/"
    list_surveys_url = "{}Demand/v1/Surveys/BySurveyStatus".format(base_url)
    reconcile_survey_url = "{}Demand/v1/Surveys/Reconcile".format(base_url)
    good_ids_list = None

    def __init__(self, api_key: str):
        """

        :param api_key:
        """
        self.api_key = api_key
        self.completed_surveys = self.list_completed_surveys()
        self.good_ids_list = self.configure_good_ids_list()

    def list_completed_surveys(self):
        """
        Queries Fulcrum API for the list of completed surveys

        :return:
        """

        request_header = {FulcrumVariables.authorization: self.api_key}
        response = requests.get("{}/{}".format(self.list_surveys_url, FulcrumVariables.complete_name),
                                headers=request_header)
        response_data = json.loads(response.json())

        return response_data.get(FulcrumVariables.survey_list_name)

    def reconcile_survey(self, survey_number):
        """
        Sends json with list of good ids for a survey to the reconciliation endpoint at the Fulcrum API

        :param survey_number: unique ID of the survey to be reconciled
        :return:
        """

        # Check that the ids list has been set
        if self.good_ids_list is None:
            raise Exception

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

        if response.status_code != 202:
            raise Exception

    def configure_good_ids_list(self):
        thing = self.api_key

        return []

    def reconcile_completed_surveys(self):
        for survey in self.completed_surveys:
            self.reconcile_survey(survey.get('survey_number'))
