from aiogram import Bot
from aiogram.types import Message
from external_services.cat import GetCatsLink
from config_data.config import Url
import os


async def process_start(message: Message, bot: Bot) -> None:
    if not os.path.exists(f"for_users/{message.chat.username}"):
        os.mkdir(f"for_users/{message.chat.username}")

    text = f"Привет, {message.chat.first_name} {message.chat.last_name}! \
Пока что мало что умею мало что, но я стремлюсь к этому! \
Действующие фуннции смотреть в /help."

    await bot.send_message(message.chat.id, text)


async def sendPhoto_cat(message: Message, bot: Bot,
                        cat_api: Url, http_cat: Url) -> None:
    await bot.send_photo(message.chat.id, GetCatsLink(cat_api, http_cat))


async def send_sticker(message: Message, bot: Bot) -> None:
    # read_message(message)
    assert message.sticker
    await bot.send_sticker(message.chat.id, message.sticker.file_id,
                           reply_to_message_id=message.message_id)


async def send_photo(message: Message, bot: Bot) -> None:
    assert message.photo
    photo_id = message.photo[-1].file_id
    photo = await bot.get_file(photo_id)
    path = f"for_users/{message.chat.username}/{message.message_id}"
    assert photo.file_path
    await bot.download_file(photo.file_path, path + ".jpg")


async def send_text(message: Message, bot: Bot) -> None:
    assert message.text
    await bot.send_message(message.chat.id, message.text)
