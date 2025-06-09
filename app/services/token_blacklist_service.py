# class TokenBlacklistService:
#     def __init__(self, redis):
#         self.redis = redis
#
#     async def add_token_to_blacklist(self, token: str, expires_in: int):
#         key = f"blacklist:{token}"
#         await self.redis.set(key, 1, ex=expires_in)
#
#     async def is_token_blacklisted(self, token: str) -> bool:
#         key = f"blacklist:{token}"
#         value = await self.redis.get(key)
#         return value is not None