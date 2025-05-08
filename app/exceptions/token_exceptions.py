class TokenNotCorrect(Exception):
    detail = 'Token is not correct'


class TokenMissingException(Exception):
    detail = 'Token is missing'

class TokenError(Exception):
    status_code = 400
    default_detail = "Ошибка токена"

    def __init__(self, detail: str = None):
        self.detail = detail or self.default_detail
        super().__init__(self.detail)


class TokenExpiredError(TokenError):
    status_code = 401
    default_detail = "Срок действия токена истёк"


class TokenBlacklistError(TokenError):
    status_code = 403
    default_detail = "Токен недействителен (находится в Blacklist)"


class TokenDecodeError(TokenError):
    status_code = 400
    default_detail = "Не удалось расшифровать токен"
