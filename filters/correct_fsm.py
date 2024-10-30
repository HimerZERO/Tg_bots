from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from database.my_english import MemoryCards, PairWords
import logging

logger = logging.getLogger(__name__)

class WordInList(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        assert message.from_user
        assert message.from_user.username
        data: dict[str, str] = await state.get_data()
        if data.get("db") is None:
            logger.error(f"'db' is not key of data: {data}")
            return False
        base = MemoryCards(data["db"])
        return message.text in [word.GetWord() for word in base.my_words]
