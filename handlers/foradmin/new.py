from aiogram import Bot, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import Message
from database.my_english import MemoryCards, PairWords
from external_services.cat import GetCatsLink
from filters import is_admin, correct_fsm
from lexicon.lexicon import LEXICON_GENERAL
import logging

logger = logging.getLogger(__name__)

router = Router()

class FSMWrireWord(StatesGroup):
    getting_word = State()

TEXT_NEW = '''
Enter a new word in the following format:
word - explanation
'''

TEXT_UNFORMAT = '''
The input didn't match the format.
Send '/close' of '/cancel' if you want to exit.
'''

@router.message(Command(commands="new"), StateFilter(default_state))
async def new_word(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(message.chat.id, TEXT_NEW)
    await state.set_state(FSMWrireWord.getting_word)

@router.message(lambda x: x.text and x.text.count(' - ') == 1,
                StateFilter(FSMWrireWord.getting_word))
async def enter_word(message: Message, bot: Bot, state: FSMContext):
    word, explanation = message.text.split(' - ')
    dictionary = MemoryCards()
    dictionary.NewWord(word, explanation)
    dictionary.Close()
    logger.info(f'{message.from_user.username} wants to add {word}: {explanation}')
    await bot.send_message(message.chat.id, f"\"{word}\" was added as \"{explanation}\"")
    await state.clear()

@router.message(StateFilter(FSMWrireWord.getting_word))
async def enter_word(message: Message, bot: Bot, state: FSMContext):
    logger.info(f'{message.from_user.username} wants to add \"{message.text}\"')
    await bot.send_message(message.chat.id, TEXT_UNFORMAT)