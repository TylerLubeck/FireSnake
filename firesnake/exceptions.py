class ValidationError(Exception):
    pass


class TooManyConditions(ValidationError):
    pass


class InvalidPriority(ValidationError):
    pass


class InvalidTimeToLive(ValidationError):
    pass


class InvalidDataKey(ValidationError):
    pass

