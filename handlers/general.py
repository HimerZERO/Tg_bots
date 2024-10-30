from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from lexicon.lexicon import LEXICON_GENERAL
import logging
import os

router = Router()
logger = logging.getLogger(__name__)

@router.message(CommandStart())
async def process_start(message: Message, bot: Bot) -> None:
    logging.info(f"{message.chat.username} joined!")
    if not os.path.exists(f"for_users/{message.chat.username}"):
        os.mkdir(f"for_users/{message.chat.username}")

    await bot.send_message(message.chat.id, LEXICON_GENERAL['/start'].format(
        fname=message.from_user.first_name,
        lname=message.from_user.last_name,
    ))

@router.message(Command(commands=['cancel', 'close']), ~StateFilter(default_state))
async def process_cancel(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(message.chat.id, "You can be free... this time")
    await state.clear()
