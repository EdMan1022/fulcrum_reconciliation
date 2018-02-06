class CustomError(Exception):
    def __init__(self):
        Exception.__init__(
            self,
            '\nParent exception for all custom exceptions for the project.\n'
            'Allows known exceptions (that tests are expecting) to be caught\n'
            'and re-raised easily by intermediate step functions.'
        )
