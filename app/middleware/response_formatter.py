import json
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response
from starlette.types import ASGIApp, Scope, Receive, Send


class ResponseFormatterMiddleware(BaseHTTPMiddleware):
    """
    Middleware для форматирования успешных 2xx ответов в единый формат API, исключая Swagger UI и OpenAPI схемы.
    """

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Scope, call_next: Receive) -> Response:
        # Исключаем маршруты Swagger UI и OpenAPI схем
        if request["path"] in ["/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Получаем ответ от следующего обработчика в цепочке
        response = await call_next(request)

        # Формируем единый формат только для успешных 2xx ответов
        if 200 <= response.status_code < 300:
            try:
                # Извлекаем тело ответа
                response_body = b"".join([section async for section in response.body_iterator])
                response_text = response_body.decode("utf-8") or "{}"
                body = json.loads(response_text)
            except (json.JSONDecodeError, AttributeError, ValueError):
                body = None

            # Формируем стандартный JSON-ответ
            response = JSONResponse(
                content={
                    "success": True,
                    "message": "Request processed successfully",
                    "data": body,
                    "status_code": response.status_code,
                },
                status_code=response.status_code,
            )

            # Удаляем заголовок Content-Length (он будет пересчитан автоматически)
            if "content-length" in response.headers:
                del response.headers["content-length"]

        return response