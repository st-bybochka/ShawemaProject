from fastapi.responses import JSONResponse


def create_response(success: bool, message: str, data: dict = None, status_code: int = 200) -> JSONResponse:
    """
    Создает унифицированный ответ для API.
    """
    content = {
        "success": success,
        "message": message,
        "data": data,
        "status_code": status_code,
    }
    return JSONResponse(content=content, status_code=status_code)
