from fulcrum_reconciliation.extensions import db
from .custom_foreign_key_classes import ForeignKeyNull

survey_status_code_association = db.Table('survey_status_code_association', db.Model.metadata,
                                          db.Column('fulcrum_survey_id', db.Integer,
                                                    ForeignKeyNull('fulcrum_survey.id')),
                                          db.Column('fulcrum_survey_status_id', db.Integer,
                                                    ForeignKeyNull('fulcrum_survey_status.id')),
                                          )


class FulcrumSurveyStatus(db.Model):
    """
    Logs existing fulcrum surveys, and tracks their completed status and reconciliation status

    Prevents possible issues of reconciling every survey that ever existed with fulcrum every time we try to
    reconcile surveys.
    """

    __table_name__ = 'fulcrum_survey_status'

    id = db.Column(db.Integer, primary_key=True)

    code = db.Column(db.Text)
    name = db.Column(db.Text)

    survey = db.relationship('FulcrumSurvey', secondary=survey_status_code_association, order_by="FulcrumSurvey.id")

    def __init__(self, code=None, name=None):
        self.code = code
        self.name = name
