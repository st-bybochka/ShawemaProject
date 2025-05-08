from typing import Annotated
from fastapi import Depends, Request, HTTPException

from app.repositories.base_repository import BaseRepository
from app.services import UserService, AuthService, HashService, JwtTokenService
from app.repositories import UserRepository
from app.config import settings
from app.services.token_blacklist_service import TokenBlacklistService


async def get_hash_service() -> HashService:
    return HashService()


async def get_blacklist_service() -> TokenBlacklistService:
    return TokenBlacklistService()


async def get_jwt_token_service(
        blacklist_service: Annotated[TokenBlacklistService, Depends(get_blacklist_service)]
) -> JwtTokenService:
    return JwtTokenService(
        settings=settings,
        blacklist_service=blacklist_service
    )


async def get_base_repository() -> BaseRepository:
    return BaseRepository()


async def get_user_repository() -> UserRepository:
    return UserRepository()


async def get_user_service(
        user_repository: Annotated[UserRepository, Depends(get_user_repository)],
        jwt_token_service: Annotated[JwtTokenService, Depends(get_jwt_token_service)],
        hash_service: Annotated[HashService, Depends(get_hash_service)]
) -> UserService:
    return UserService(
        user_repository=user_repository,
        jwt_token_service=jwt_token_service,
        hash_service=hash_service,
    )


async def get_auth_service(
        user_repository: Annotated[UserRepository, Depends(get_user_repository)],
        hash_service: Annotated[HashService, Depends(get_hash_service)],
        jwt_token_service: Annotated[JwtTokenService, Depends(get_jwt_token_service)],
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        hash_service=hash_service,
        jwt_token_service=jwt_token_service,
        settings=settings,
    )


async def get_current_token(
        request: Request,
        jwt_token_service: JwtTokenService = Depends(get_jwt_token_service)
) -> str:

    token = request.cookies.get("access_token")

    # Если токен отсутствует в cookies — возвращаем ошибку
    if not token:
        raise HTTPException(status_code=401, detail="Токен авторизации отсутствует")

    try:
        await jwt_token_service.decode_token(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Невалидный токен: {str(e)}")

    return token

