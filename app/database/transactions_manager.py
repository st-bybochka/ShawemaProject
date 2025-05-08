class TransactionManager:
    def __init__(self, async_session_maker):
        self.async_session_maker = async_session_maker

    async def __aenter__(self):
        self.session = self.async_session_maker()  # Создаём сессию
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:

            await self.session.commit()
        else:

            await self.session.rollback()
        await self.session.close()
