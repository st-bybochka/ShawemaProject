from fastapi import Response
from dataclasses import dataclass

from app.repositories import UserRepository
from app.schemas import UserLoginSchema
from app.services.hash_service import HashService
from app.services.jwt_token_service import JwtTokenService
from app.exceptions import UserAlreadyRegisteredException, UserNotFoundException


@dataclass
class UserService:
    user_repository: UserRepository
    jwt_token_service: JwtTokenService
    hash_service: HashService

    async def create_user(self, response: Response, data: UserLoginSchema) -> None:

        user = await self.user_repository.get_user_by_email(str(data.email))

        if user:
            raise UserAlreadyRegisteredException

        hashed_password = self.hash_service.get_hash_password(data.hashed_password)

        user_id = await self.user_repository.create_user(str(data.email), hashed_password)

        access_token = await self.jwt_token_service.create_access_token(user_id=user_id)
        refresh_token = await self.jwt_token_service.create_refresh_token(user_id=user_id)

        response.set_cookie(key="refresh_token", value=str(refresh_token), httponly=True)
        response.set_cookie(key="access_token", value=str(access_token), httponly=True)





