import asyncio
import logging
import logging.config

from aiogram import F
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram.types import Message
from config_data.config import Config, load_config
import handlers
import requests
import os

import handlers.general


async def process_help(message: Message, bot: Bot) -> None:
    await bot.send_message(message.chat.id,
                           "/start - Приветствие :)\n"
                           "/help - Выдаёт список доступных команд\n"
                           "/cat - отправляет фотку с котиком ^^~\n"
                           "/solved - инструкция к сдаче\n"
                           )


async def start_to_solved(message: Message, bot: Bot) -> None:
    await bot.send_message(message.chat.id,
                           "Напиши решение в "
                           "следующем формате:")
    await bot.send_message(message.chat.id,
                           "/Прикрепляешь фото, ровно одно!/\n"
                           "/solved\n"
                           "<Какой то комментарий про то, "
                           "какая именно эта задача>\n"
                           "<Необязательный комментарий к решению>"
                           )


async def solved(message: Message, bot: Bot) -> None:
    assert message.photo
    assert message.caption
    os.mkdir(f"for_users/{message.chat.username}/{message.message_id}")
    photo_id = message.photo[-1].file_id
    photo = await bot.get_file(photo_id)
    assert photo.file_path
    path = f"for_users/{message.chat.username}/{message.message_id}"
    await bot.download_file(photo.file_path, path + '/photo.jpg')
    with open(path + "/commit.txt", "w") as fp:
        fp.write(message.caption)
    await bot.send_message(message.chat.id, "Задача принята на проверку!")

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s'
               '[%(asctime)s] %(message)s'
    )
    logger.info('Starting bot')

    config: Config = load_config()

    redis = Redis(host='localhost')

    storage = RedisStorage(redis=redis)

    my_token = config.bot.token
    cat_api = config.urls["CAT_API"]
    tg_api = config.urls["TG_API"]
    http_cat = config.urls["HTTP_CAT"]
    admins = config.bot.admins

    logger.info(admins)

    bot = Bot(token=my_token)
    dp = Dispatcher(storage=storage)

    dp.include_router(handlers.general.router)
    dp.include_router(handlers.admin.router)
    dp.include_router(handlers.user.router)

    dp.workflow_data.update({
            "cat_api": cat_api,
            "tg_api": tg_api,
            "http_cat": http_cat,
            "admins": admins,
        }
    )
    # dp.message.register(process_help, Command(commands="help"))
    dp.message.register(start_to_solved, lambda x: x.text == "/solved")
    dp.message.register(solved, Command(commands="solved"))

    await dp.start_polling(bot)

asyncio.run(main())
