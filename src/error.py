
class _Error(Exception):
    message = ""

    def __init__(self, message):
        self.message = message


class BadRequestError(_Error):
    pass


class NotFoundError(_Error):
    pass


class DBError(_Error):
    def __init__(self, code):
        self.message = "SQL error: " + str(code)


class ValidationError(_Error):
    pass
