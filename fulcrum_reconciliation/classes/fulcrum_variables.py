class FulcrumVariables(object):
    """
    Contains constants for the Fulcrum API

    :attribute completed_survey_code (str): Survey code that classifies a survey as completed
    :attribute authorization (str): Text value of the header key that contains the api authorization key
    :attribute complete_name (str): Text value of the survey status that refers to a complete survey
    :attribute survey_list_name (str): Text value of the key in the list_surveys response that holds the list of surveys
    :attribute response_ids (str): Text value of the key coding for the list of good ids in the request header
    :attribute reconciliation_response_code (list): List of valid response codes for the reconciliation end point
    """

    completed_survey_code = '04'
    authorization = "Authorization"
    complete_name = "Completed"
    survey_list_name = "Surveys"
    survey_status_key = 'SurveyStatusCode'
    response_ids = "ResponseIDs"
    survey_number = 'SurveyNumber'
    reconciliation_response_code = [202]
    survey_name = "SurveyName"

    all_survey_status_codes = ['01', '02', '03', '04', '05', '06']

