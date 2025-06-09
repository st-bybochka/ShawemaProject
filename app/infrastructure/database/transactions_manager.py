from functools import wraps

from sqlalchemy.ext.asyncio import async_sessionmaker
from app.infrastructure.database.database import async_session_maker


class Transactional:
    def __init__(self, session_maker: async_sessionmaker):
        self.session_maker = session_maker

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            async with self.session_maker() as session:
                async with session.begin():
                    try:

                        return await func(*args, session=session, **kwargs)
                    except Exception:
                        await session.rollback()
                        raise
        return wrapper

transaction = Transactional(async_session_maker)
