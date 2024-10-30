from aiogram import Bot, Router
from aiogram.types import Message
from aiogram.filters import Command
from external_services.cat import GetCatsLink
from config_data.config import Url
from lexicon.lexicon import LEXICON_GENERAL

router = Router()

@router.message(Command(commands="cat"))
async def sendPhoto_cat(message: Message, bot: Bot,
                        cat_api: Url, http_cat: Url) -> None:
    await bot.send_photo(message.chat.id, GetCatsLink(cat_api, http_cat))
