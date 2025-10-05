from typing import TYPE_CHECKING
from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from keyboards.inline import fact_again_keyboard, persons_keyboard, topic_keyboard, qviz_answer_keyboard
from services.dialog_with_person import get_persona_response
from services.quiz_service import get_quiz_question, check_answer
from services.random_fact import get_fact
from storage import dialogues, PERSONS



router = Router()


class QuizStates(StatesGroup):
    waiting_answer = State()
    waiting_question = State()
    in_quiz = State()


class FactStates(StatesGroup):
    waiting_fact = State()


if TYPE_CHECKING:
    from aiogram.types import CallbackQuery
    from aiogram.fsm.context import FSMContext


@router.callback_query(F.data == 'random_fact')
async def random_handler(call: CallbackQuery, state: FSMContext):
    await state.set_state(FactStates.waiting_fact)
    await call.message.answer("⏳ Загружаю интересный факт...")
    fact = await get_fact()
    await call.message.answer(f"{fact}", reply_markup=fact_again_keyboard())


PERSONA_NAMES = {
    'shakespeare': 'Шекспир',
    'einstein': 'Эйнштейном',
    'lermontov': 'Лермонтовым'
}


@router.callback_query(F.data == 'persona')
async def persona_handler(call: CallbackQuery):
    await call.message.edit_text("🎭 Выбери персонажа для общения:", reply_markup=persons_keyboard())


@router.callback_query(
    F.data.startswith('shakespeare') |
    F.data.startswith('einstein') |
    F.data.startswith('lermontov')
)
async def persona_selection_handler(call: CallbackQuery, state: FSMContext):
    """Обрабатывает выбор персонажа и начинает диалог"""
    await call.answer()

    persona = call.data
    thinking_msg = await call.message.answer("🔄 Персонаж обдумывает ответ...")

    user_message = "Расскажи что-нибудь интересное о себе и своем творчестве"
    response = await get_persona_response(persona, user_message)

    await call.message.answer(response)

    if call.from_user.id not in dialogues:
        dialogues[call.from_user.id] = []

    dialogues[call.from_user.id].extend([
        {'role': "system", 'content': PERSONS[persona]},
        {'role': "user", 'content': user_message},
        {'role': "assistant", 'content': response}
    ])


@router.callback_query(F.data == 'close_keyboard')
async def close_handler(call: CallbackQuery):
    await call.answer("Диалог закрыт", show_alert=True)
    await call.message.delete()


user_data = {}


@router.callback_query(F.data == "quiz")
async def quiz_handler(call: CallbackQuery):
    user_id = call.from_user.id
    user_data[user_id] = {"score": 0}
    await call.message.answer("Выбери тему:", reply_markup=topic_keyboard())
    await call.answer()



@router.callback_query(
    F.data.startswith("topic:history") |
    F.data.startswith("topic:it") |
    F.data.startswith("topic:science")
)
async def quiz_topic_handler(call: CallbackQuery):
    user_id = call.from_user.id
    topic = call.data.split(":")[1]


    if user_id not in user_data:
        user_data[user_id] = {
            "score": 0,
            "topic": topic
        }
    else:
        user_data[user_id]["topic"] = topic


    question = await get_quiz_question(topic)
    user_data[user_id]["current_question"] = question

    await call.message.edit_text(f"❓\n{question}")
    await call.answer()



@router.message(F.text)
async def answer_handler(message: Message):
    user_id = message.from_user.id

    if user_id not in user_data:
        return

    data = user_data[user_id]
    question = data.get("current_question")
    user_answer = message.text

    if not question:
        await message.answer("Сначала выбери тему!")
        return

    result = await check_answer(question, user_answer)

    if "правильно" in result.lower():
        data["score"] += 1
        await message.answer(f"✅ Правильно! Счет: {data['score']}", reply_markup=qviz_answer_keyboard())
    else:
        await message.answer(f"❌ Неправильно! Счет: {data['score']}", reply_markup=qviz_answer_keyboard())


@router.callback_query(F.data == "next_question")
async def next_question_handler(call: CallbackQuery):
    user_id = call.from_user.id

    if user_id not in user_data:
        await call.message.answer("Сначала начни викторину!")
        await call.answer()
        return

    data = user_data[user_id]
    topic = data.get("topic")

    if not topic:
        await call.message.answer("Сначала выбери тему!")
        await call.answer()
        return

    question = await get_quiz_question(topic)
    data["current_question"] = question

    await call.message.edit_text(f"❓\n{question}")
    await call.answer()


@router.callback_query(F.data == "change_topic")
async def change_topic_handler(call: CallbackQuery):
    user_id = call.from_user.id

    if user_id in user_data:
        # Сохраняем счет, но сбрасываем текущий вопрос
        user_data[user_id]["current_question"] = None

    await call.message.edit_text("Выбери тему:", reply_markup=topic_keyboard())
    await call.answer()


@router.callback_query(F.data == "end_quiz")
async def end_quiz_handler(call: CallbackQuery):
    user_id = call.from_user.id

    if user_id in user_data:
        score = user_data[user_id].get("score", 0)
        await call.message.edit_text(f"🏁 Викторина завершена!\n\nТвой счет: {score}")
        # Удаляем данные пользователя
        del user_data[user_id]
    else:
        await call.message.edit_text("Викторина завершена!")

    await call.answer()


