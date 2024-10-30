from aiogram import Bot, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import Message
from database.my_english import MemoryCards, PairWords
from external_services.cat import GetCatsLink
from filters import is_admin, correct_fsm
from handlers.foradmin import getlist, new, check
from lexicon.lexicon import LEXICON_GENERAL
import logging

logger = logging.getLogger(__name__)

router = Router()

router.message.filter(is_admin.IsAdmin())

router.include_router(new.router)
router.include_router(getlist.router)
router.include_router(check.router)

TEXT_HELP = '''
/cancel /close (Выйти из состояния)
/new (Добавить слово в словарь)
/list (Показать все слова в словаре)
/list_order (Показать все слова в словаре по возрастанию прогресса)
/check (Проверка на знание слова)
'''

TEXT_UNFORMAT = '''
The input didn't match the format.
Send '/close' of '/cancel' if you want to exit.
'''

@router.message(Command(commands="help"))
async def process_help(message: Message, bot: Bot, admins: list[str]):
    logger.info(f'{message.from_user.username} loggin as Admin')
    logger.debug(f"all admons:  {admins}")
    await bot.send_message(message.chat.id, "You is Admin")
    await bot.send_message(message.chat.id, TEXT_HELP)

'''
@router.message(StateFilter(FSMWrireWord.show_list))
async def enter_word(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(message.chat.id, TEXT_UNFORMAT)'''
