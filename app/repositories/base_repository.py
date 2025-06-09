from sqlalchemy import select

from app.infrastructure.database.transactions_manager import transaction


class BaseRepository:
    model = None

    @transaction
    async def get_one_or_none(self, session, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @transaction
    async def get_by_id(self, session, model_id: int):
        query = select(self.model).filter_by(id=model_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @transaction
    async def get_all(self, session, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().all()

    @transaction
    async def create(self, session, model):
        session.add(model)

    @transaction
    async def update(self, session, model):
        session.add(model)

    @transaction
    async def delete(self, session, model):
        await session.delete(model)
