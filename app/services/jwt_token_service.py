from jose import jwt, JWTError, ExpiredSignatureError
from dataclasses import dataclass

from datetime import datetime, timedelta
from typing import Literal

from app.config import settings
from app.exceptions import TokenExpiredError, TokenBlacklistError, TokenDecodeError
from app.services.token_blacklist_service import TokenBlacklistService


@dataclass
class JwtTokenService:
    settings: settings
    blacklist_service: TokenBlacklistService

    async def _create_token(self, user_id: int, token_type: Literal["access", "refresh"]) -> str:
        if token_type == "access":
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        elif token_type == "refresh":
            expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        to_encode = {"user_id": user_id, "exp": expire}
        return jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.ALGORITHM
        )

    async def create_access_token(self, user_id: int) -> str:
        return await self._create_token(user_id, "access")

    async def create_refresh_token(self, user_id: int) -> str:
        return await self._create_token(user_id, "refresh")

    async def decode_token(self, token: str) -> dict:

        is_blacklisted = await self.blacklist_service.is_token_blacklisted(token)
        if is_blacklisted:
            raise TokenBlacklistError()

        try:
            # Попытка декодировать токен
            decoded_data = jwt.decode(
                token,
                self.settings.JWT_SECRET_KEY,
                algorithms=[self.settings.ALGORITHM]
            )
        except ExpiredSignatureError:
            raise TokenExpiredError()
        except JWTError:
            raise TokenDecodeError()

        return decoded_data


