import flask
from fulcrum_reconciliation.classes import FulcrumVariables, AutoReconciler, DbVariables
from fulcrum_reconciliation.extensions import db
from fulcrum_reconciliation import models
import datetime

survey_management_bp = flask.Blueprint('survey_management_bp', __name__)


@survey_management_bp.route('/survey_management/update_all_surveys')
def update_all_surveys_view():
    """
    Update the survey statuses in the database with data from the Fulcrum API

    :return:
    """

    config = db.app.config
    api_helper = AutoReconciler(api_key=config.get('API_KEY'), base_url=config.get('BASE_URL'))

    for survey_status_code in FulcrumVariables.all_survey_status_codes:
        survey_list = api_helper.list_surveys_by_status(survey_status=survey_status_code)

        for fulcrum_survey in survey_list:

            db_survey = models.FulcrumSurvey.query.filter_by(
                survey_number=fulcrum_survey.get(FulcrumVariables.survey_number)).first()
            if db_survey:
                if db_survey.survey_status_code != fulcrum_survey.get(FulcrumVariables.survey_status_key):
                    db_survey.survey_status_code = fulcrum_survey.get(FulcrumVariables.survey_status_key)
                    db.session.flush()
            else:
                new_survey = models.FulcrumSurvey(survey_number=fulcrum_survey.get(FulcrumVariables.survey_number),
                                                  name=fulcrum_survey.get(FulcrumVariables.survey_name),
                                                  survey_status_code=fulcrum_survey.get(
                                                      FulcrumVariables.survey_status_key),
                                                  reconciliation_status_code=DbVariables.not_reconciled_code)
                db.session.add(new_survey)
                db.session.flush()
        db.session.commit()

    return 'Update Complete'


@survey_management_bp.route('/survey_management/configure_previous_month_ids')
def configure_previous_month_ids_view():

    config = db.app.config
    api_helper = AutoReconciler(api_key=config.get('API_KEY'), base_url=config.get('BASE_URL'))

    today = datetime.datetime.today()
    first_of_month = today.replace(day=1)
    last_month = first_of_month - datetime.timedelta(days=2)

    api_helper.configure_month_good_ids_file(month=last_month.month, year=last_month.year,
                                             month_str=datetime.datetime.strftime(last_month, '%B'))
    return 'Previous Month IDs Created'


@survey_management_bp.route('/survey_management/reconcile_surveys')
def reconcile_surveys_view():
    """
    Performs reconciliation function for surveys that are complete but not yet reconciled

    :return:
    """

    config = db.app.config
    api_helper = AutoReconciler(api_key=config.get('API_KEY'), base_url=config.get('BASE_URL'))

    api_helper.configure_good_ids_list()
    api_helper.configure_reconciliation_list()

    api_helper.reconcile_completed_surveys()

    return 'Reconciliation Complete'
