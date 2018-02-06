from fulcrum_reconciliation.extensions import db


class FulcrumSurvey(db.Model):
    """
    Logs existing fulcrum surveys, and tracks their completed status and reconciliation status

    Prevents possible issues of reconciling every survey that ever existed with fulcrum every time we try to
    reconcile surveys.
    """

    __table_name__ = 'fulcrum_survey'
    id = db.Column(db.Integer, primary_key=True)
    survey_number = db.Column(db.Integer, unique=True)
    name = db.Column(db.Text)
    reconciliation_status_code = db.Column(db.Text)
    survey_status_code = db.Column(db.Text)

    def __init__(self, survey_number=None, name=None, reconciliation_status_code=None,
                 survey_status_code=None):
        self.survey_number = survey_number
        self.name = name
        self.reconciliation_status_code = reconciliation_status_code
        self.survey_status_code = survey_status_code
