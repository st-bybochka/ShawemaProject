from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base_repository import BaseRepository
from app.services import UserService, AuthService, HashService, JwtTokenService
from app.repositories import UserRepository
from app.database import get_async_session
from app.config import settings


async def get_hash_service() -> HashService:
    return HashService()


async def get_jwt_token_service() -> JwtTokenService:
    return JwtTokenService()


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
