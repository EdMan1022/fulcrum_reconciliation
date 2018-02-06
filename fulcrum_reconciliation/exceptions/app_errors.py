from .custom_exception import CustomError


class NoAppConfigError(CustomError):
    def __init__(self):
        Exception.__init__(self, "No config provided to create app.")
