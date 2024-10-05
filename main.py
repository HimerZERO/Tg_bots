from aiogram import F
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import requests

with open("passwords/token.tg", 'r', encoding="utf-8") as fp:
    my_token: str = fp.read()
with open("passwords/url_api.tg", 'r', encoding="utf-8") as fp:
    tg_api: str = fp.read()
with open("passwords/url_api.cat", 'r', encoding="utf-8") as fp:
    cat_api: str = fp.read()
timeout = 30

bot = Bot(token=my_token)
dp = Dispatcher()


async def process_start(message: Message) -> None:
    await bot.send_message(message.chat.id, "Hello, my new friend. I can"
                           " help you with your tasks")


async def process_help(message: Message) -> None:
    await bot.send_message(message.chat.id, "If you send me a text, I"
                           " will send it is you")


async def sendPhoto_cat(message: Message) -> None:
    cat_response: requests.Response = requests.get(cat_api)
    print(cat_response.status_code)
    if cat_response.status_code == 200:
        cat_link: str = cat_response.json()[0]['url']
        await bot.send_photo(message.chat.id, cat_link)
    else:
        await bot.send_photo(message.chat.id,
                             f'https://http.cat/{cat_response.status_code}')


async def send_text(message: Message) -> None:
    assert message.text
    await bot.send_message(message.chat.id, message.text)


async def send_sticker(message: Message) -> None:
    assert message.sticker
    await bot.send_sticker(message.chat.id, message.sticker.file_id,
                           reply_to_message_id=message.message_id)


async def send_sorry():
    pass


dp.message.register(process_start, Command(commands="start"))
dp.message.register(process_help, Command(commands="help"))
dp.message.register(sendPhoto_cat, Command(commands="cat"))
dp.message.register(send_text, F.text)
dp.message.register(send_sticker, F.sticker)

if __name__ == "__main__":
    dp.run_polling(bot)
