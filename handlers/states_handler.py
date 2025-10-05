from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from handlers.quiz_manager import increase_score, get_score
from keyboards.inline import topic_keyboard, qviz_answer_keyboard
from services.quiz_service import check_answer
from services.role_mod import ask_role_gpt
from states import Person, GPTDialog, MessageTalks, QuizStates
from storage import dialogues


router = Router()


@router.message(MessageTalks.message)
async def message_handler(message: Message):
    answer = await ask_role_gpt(message.from_user.id, message.text)
    persona = dialogues[message.from_user.id]['persona']
    await message.answer(f'Answer - {answer}'())

@router.message(Command('quiz'))
async def quiz_handler(message: Message, state: FSMContext):
    await state.set_state(QuizStates.choosing_topic)
    await message.answer("Выбери тему викторины:", reply_markup=topic_keyboard())



