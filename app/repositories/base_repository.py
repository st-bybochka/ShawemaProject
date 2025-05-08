from sqlalchemy import select

from app.infrastructure.database.database import async_session_maker



class BaseRepository:
    model = None


    async def get_one_or_none(self, **filter_by):
        async with async_session_maker() as session:

            query = select(self.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_by_id(self, model_id: int):
        async with async_session_maker() as session:

            query = select(self.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_all(self, **filter_by):
        async with async_session_maker() as session:
            query = select(self.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    async def create(self, model):
        async with async_session_maker() as session:
            session.add(model)
            await session.commit()

    async def update(self, model):
        async with async_session_maker() as session:
            session.add(model)
            await session.commit()

    async def delete(self, model):
        async with async_session_maker() as session:
            await session.delete(model)
            await session.commit()
