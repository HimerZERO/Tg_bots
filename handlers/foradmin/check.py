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
    in_game = State()
    end_game = State()

TEXT_GAME = '''
Send '/close' of '/cancel' if you want to exit.
Give an explanation of ...
'''

TEXT_YES = '''
Yes, is right!
'''

TEXT_NO = '''
Wrong answer :(
The correct answer is {correct}
'''

@router.message(StateFilter(default_state), Command(commands="check"))
async def start_game(message: Message, bot: Bot, state: FSMContext):
    dictionary = MemoryCards()
    words: list[PairWords] = dictionary.GetWeightRandom()
    if not words:
      logger.warning(f'{message.from_user.username} accessed an empty dictionary')
      await bot.send_message(message.chat.id, "The dictionary is empty")
      return
    await bot.send_message(message.chat.id, TEXT_GAME)
    word: PairWords = words[0]
    await bot.send_message(message.chat.id, word.GetWord())
    await state.set_state(FSMWrireWord.in_game)
    await state.update_data(db=dictionary.GetDataBase(), word=word.GetWord())

@router.message(StateFilter(FSMWrireWord.in_game))
async def during_game(message: Message, bot: Bot, state: FSMContext):
    data : dict[str, str] = await state.get_data()
    data_base = MemoryCards(data['db'])
    word = data['word']
    if (data_base is None or word is None):
        logger.error(f"...?")
        await bot.send_message(message.chat.id, "...")
        return
    pair = data_base.GetPair(word)
    correct_answer = pair.GetExplanation()
    if pair.CheckAnswer(message.text):
        await bot.send_message(message.chat.id, TEXT_YES)
    else:
        await bot.send_message(message.chat.id, TEXT_NO.format(correct=correct_answer))
    data_base.Close()

    await start_game(message, bot, state)
