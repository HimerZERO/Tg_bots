from aiogram.filters import BaseFilter
from aiogram.types import Message

class IsAdmin(BaseFilter):
    async def __call__(self, message: Message, admins: list[str]) -> bool:
        assert message.from_user
        assert message.from_user.username
        return message.from_user.username in admins
