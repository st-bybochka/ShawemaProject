from dataclasses import dataclass
from fastapi import Response, Request
from datetime import datetime, timedelta
from jose import JWTError, jwt

from app.repositories import UserRepository
from app.config import settings
from app.exceptions import (UserNotFoundException, UserIncorrectLoginOrPasswordException,
                            TokenMissingException, TokenNotCorrect, UserBlockedException)
from app.schemas import UserLoginSchema
from app.models import UserProfile

from app.services.hash_service import HashService
from app.services.jwt_token_service import JwtTokenService


@dataclass
class AuthService:
    user_repository: UserRepository
    jwt_token_service: JwtTokenService
    hash_service: HashService
    settings: settings

    async def login(self, data: UserLoginSchema, response: Response) -> dict:
        user = await self._authenticate_user(data=data)
        await self._check_block_status(user=user)
        tokens = await self._generate_tokens(user_id=user.id, response=response)
        return tokens

    async def logout(self, token: str):

        decoded_token = await self.jwt_token_service.decode_token(token=token)
        exp = decoded_token["exp"]
        current_time = datetime.utcnow().timestamp()

        expires_in = int(exp - current_time)
        if expires_in > 0:
            await self.jwt_token_service.blacklist_service.add_token_to_blacklist(token, expires_in)

    async def refresh_access_token(self, request: Request, response: Response):

        refresh_token = request.cookies.get("refresh_token")

        if not refresh_token:
            raise TokenMissingException

        user_id = await self.jwt_token_service.decode_token(refresh_token)

        access_token = await self.jwt_token_service.create_access_token(user_id)
        response.set_cookie(key="access_token", value=access_token, httponly=True)

        return {"access_token": access_token, "refresh_token": refresh_token}

    async def generate_access_token(self, user_id: int) -> str:
        expire_date_unix = (datetime.utcnow() + timedelta(hours=30)).timestamp()
        token = jwt.encode(
            {"user_id": user_id, "exp": expire_date_unix},
            self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.ALGORITHM
        )
        return token

    async def get_user_id_from_access_token(self, access_token: str) -> int:

        if not access_token:
            raise TokenMissingException

        try:
            payload = jwt.decode(
                access_token,
                self.settings.JWT_SECRET_KEY,
                algorithms=[self.settings.JWT_ALGORITHM]
            )

        except JWTError:
            raise TokenNotCorrect

        return payload["user_id"]

    async def _authenticate_user(self, data: UserLoginSchema) -> UserProfile:
        user = await self.user_repository.get_user_by_email(email=str(data.email))
        if not user:
            raise UserNotFoundException(f"User with email {data.email} not found.")
        if not self.hash_service.verify_hash_password(plain_password=data.hashed_password, hashed_password=user.hashed_password):
            await self._register_failed_attempt(user=user)
            raise UserIncorrectLoginOrPasswordException
        return user

    async def _register_failed_attempt(self, user: UserProfile) -> None:

        user.login_attempts += 1
        if user.login_attempts >= 5:
            user.block_until = datetime.utcnow() + timedelta(minutes=5)
            user.login_attempts = 0
        await self.user_repository.update(user)

    async def _check_block_status(self, user: UserProfile) -> None:
        if user.block_until and user.block_until > datetime.utcnow():
            raise UserBlockedException("User is blocked. Try again later.")

    async def _generate_tokens(self, user_id: int, response: Response) -> dict:
        access_token = await self.jwt_token_service.create_access_token(user_id=user_id)
        refresh_token = await self.jwt_token_service.create_refresh_token(user_id=user_id)

        response.set_cookie(key="access_token", value=str(access_token), httponly=True, secure=True)
        response.set_cookie(key="refresh_token", value=str(refresh_token), httponly=True, secure=True)
        return {"access_token": access_token, "refresh_token": refresh_token}
