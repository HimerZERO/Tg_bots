from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsAdmin(BaseFilter):
    def __init__(self, admins: list[str]) -> None:
        self.admins = admins

    async def __call__(self, message: Message) -> bool:
        assert message.from_user
        assert message.from_user.username
        return message.from_user.username in self.admins
