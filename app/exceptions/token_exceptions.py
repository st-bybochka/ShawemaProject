class TokenNotCorrect(Exception):
    detail = 'Token is not correct'


class TokenMissingException(Exception):
    detail = 'Token is missing'