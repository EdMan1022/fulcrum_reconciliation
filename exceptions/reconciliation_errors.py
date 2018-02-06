from .custom_exception import CustomError


class NoCompleteSurveysError(CustomError):
    def __init__(self):
        Exception.__init__(self, "No complete surveys returned.")


class NoGoodIDsError(CustomError):
    def __init__(self):
        Exception.__init__(self, "No good ids found for the given month")


class ReconciliationResponseError(CustomError):
    def __init__(self, response_code):
        Exception.__init__(self, "Reconciliation route returned an invalid code: {}".format(response_code))
