from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models import UserProfile
from app.repositories.base_repository import BaseRepository
from app.exceptions import UserAlreadyRegisteredException
from app.infrastructure.database.database import async_session_maker
from app.infrastructure.database.transactions_manager import transaction


class UserRepository(BaseRepository):
    model = UserProfile

    @transaction
    async def get_user_by_email(self, session, email: str) -> UserProfile | None:
        query = select(self.model).filter_by(email=email)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @transaction
    async def create_user(self, session, email: str, hashed_password: str) -> int:
        user = self.model(
            email=email,
            hashed_password=hashed_password,

        )
        session.add(user)
        return user.id

    async def update_user(self, user: UserProfile):
        await self.update(user)
