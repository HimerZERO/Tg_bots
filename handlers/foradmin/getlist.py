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
    show_list = State()

TEXT_LIST = '''
Seved words:
(If you want to see an explanation, enter the word, else send '/close')
'''

TEXT_UNFORMAT = '''
The input didn't match the format.
Send '/close' of '/cancel' if you want to exit.
'''

@router.message(StateFilter(default_state), Command(commands="list"))
async def write_list(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(message.chat.id, TEXT_LIST)
    dictionary = MemoryCards()
    words: list[PairWords] = dictionary.AlphabetOrder()
    logger.info('\n'.join([word.GetWord() for word in words]))
    await bot.send_message(message.chat.id, '\n'.join([word.GetWord() for word in words]))
    await state.set_state(FSMWrireWord.show_list)
    await state.update_data(db=dictionary.GetDataBase())

@router.message(StateFilter(default_state), Command(commands="list_order"))
async def write_list(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(message.chat.id, TEXT_LIST)
    dictionary = MemoryCards()
    words: list[PairWords] = dictionary.NegativeProgressOrder()
    logger.info('\n'.join([word.GetWord() for word in words]))
    await bot.send_message(message.chat.id, '\n'.join([word.GetWord() for word in words]))
    await state.set_state(FSMWrireWord.show_list)
    await state.update_data(db=dictionary.GetDataBase())

@router.message(StateFilter(FSMWrireWord.show_list), correct_fsm.WordInList())
async def write_list(message: Message, bot: Bot, state: FSMContext):
    data : dict[str, str] = await state.get_data()
    explanation = MemoryCards(data['db']).GetExplanation(message.text)
    if (explanation is None):
        logger.error(f"{message.text} not in DataBase")
        await bot.send_message(message.chat.id, "...")
        return
    await bot.send_message(message.chat.id, explanation)

@router.message(StateFilter(FSMWrireWord.show_list))
async def enter_word(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(message.chat.id, TEXT_UNFORMAT)