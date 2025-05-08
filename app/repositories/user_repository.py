from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models import UserProfile
from app.repositories.base_repository import BaseRepository
from app.exceptions import UserAlreadyRegisteredException
from app.infrastructure.database.database import async_session_maker


class UserRepository(BaseRepository):
    model = UserProfile

    async def get_user_by_email(self, email: str) -> UserProfile | None:
        async with async_session_maker() as session:

            try:
                query = select(self.model).where(self.model.email == email)
                result = await session.execute(query)
                return result.scalar_one_or_none()
            except SQLAlchemyError as exc:
                raise RuntimeError("Error occurred while fetching user by email.") from exc

    async def create_user(self, email: str, hashed_password: str) -> int:
        async with async_session_maker() as session:

            try:
                user = self.model(
                    email=email,
                    hashed_password=hashed_password,
                    login_attempts=0,
                    block_until=None,
                )
                session.add(user)
                await session.commit()  # Фиксируем изменения
                return user.id
            except IntegrityError as exc:
                await session.rollback()  # Откат транзакции
                raise UserAlreadyRegisteredException(f"User with email '{email}' already exists.") from exc
            except SQLAlchemyError as exc:
                await session.rollback()
                raise RuntimeError("Error occurred while creating user.") from exc

    async def update_user(self, user: UserProfile):

        try:
            self.session.add(user)
            await self.session.commit()
        except SQLAlchemyError as exc:
            await self.session.rollback()
            raise RuntimeError(f"Error occurred while updating user with ID {user.id}.") from exc
