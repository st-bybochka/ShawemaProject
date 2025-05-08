from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from app.exceptions.user_exceptions import BaseUserException
from app.exceptions.token_exceptions import TokenNotCorrect, TokenMissingException


async def custom_http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "data": None,
            "status_code": exc.status_code,
        },
    )


async def custom_user_exception_handler(request: Request, exc: BaseUserException) -> JSONResponse:

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "data": None,
            "status_code": exc.status_code,
        },
    )


async def custom_token_exception_handler(request: Request,
                                         exc: (TokenNotCorrect, TokenMissingException)) -> JSONResponse:

    return JSONResponse(
        status_code=401,
        content={
            "success": False,
            "message": str(exc.detail),
            "data": None,
            "status_code": 401,
        },
    )


async def custom_generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error",
            "data": None,
            "status_code": 500,
        },
    )