class ValidationError(Exception):
    pass


class ValidationArgumentsError(ValidationError):
    pass


class ValidationReturnError(ValidationError):
    pass
