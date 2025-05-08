from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from app.middleware.response_formatter import ResponseFormatterMiddleware
from app.exceptions.handlers import (
    custom_http_exception_handler,
    custom_user_exception_handler,
    custom_generic_exception_handler,
    custom_token_exception_handler,
)
from app.exceptions.user_exceptions import BaseUserException
from app.exceptions.token_exceptions import TokenNotCorrect, TokenMissingException
from app.handlers import user_handler, auth_handler

app = FastAPI()

app.add_middleware(ResponseFormatterMiddleware)

# Обработчики ошибок
app.add_exception_handler(HTTPException, custom_http_exception_handler)
app.add_exception_handler(BaseUserException, custom_user_exception_handler)
app.add_exception_handler(TokenNotCorrect, custom_token_exception_handler)
app.add_exception_handler(TokenMissingException, custom_token_exception_handler)
app.add_exception_handler(Exception, custom_generic_exception_handler)

# Подключаем Middleware для формата ответов


# Роутеры
app.include_router(user_handler.router)
app.include_router(auth_handler.router)