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


@dp.message(Command(commands=['start']))
async def process_start(message: Message) -> None:
    await bot.send_message(message.chat.id, "Hello, my new friend. I can"
                           " help you with your tasks")


@dp.message(Command(commands=['help']))
async def process_help(message: Message) -> None:
    await bot.send_message(message.chat.id, "If you send me a text, I"
                           " will send it is you")


@dp.message(Command(commands=['cat']))
async def sendPhoto_cat(message: Message) -> None:
    cat_response: requests.Response = requests.get(cat_api)
    assert cat_response == 200
    cat_link: str = cat_response.json()[0]['url']
    await bot.send_photo(message.chat.id, cat_link)


@dp.message()
async def send_it(message: Message) -> None:
    await bot.send_message(message.chat.id, message.text)


if __name__ == "__main__":
    dp.run_polling(bot)
