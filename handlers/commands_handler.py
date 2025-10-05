import aiogram
from aiogram import Router,F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup  # Правильный импорт
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import types
from aiogram.filters import CommandStart
from keyboards.inline import persons_keyboard, topic_keyboard, start_keyboard
from services.dialog_gpt import dialog_gpt_func
from services.random_fact import get_fact
from states import GPTDialog, Talk  # Предполагается, что эти состояния определены в states.py
from aiogram import Bot
from aiogram.types import BotCommand, MenuButtonCommands, MenuButtonWebApp, MenuButtonDefault

router = Router()

# Если состояния GPTDialog и Talk не определены в states.py, определите их здесь:
class GPTDialog(StatesGroup):
    message = State()
#
class Talk(StatesGroup):
    persona = State()


async def set_menu_button(bot: Bot):
    # Вариант 1: Кнопка с командами (по умолчанию)
    await bot.set_chat_menu_button(
        menu_button=MenuButtonCommands()
    )

    commands = [
    BotCommand(command="start", description="🚀 Главное меню"),

    ]
    await bot.set_my_commands(commands)


@router.message(CommandStart())
@router.message(F.text == "🚀 Старт")
async def start_command(message: Message):
    await message.answer(text = "МЕНЮ БОТА", reply_markup=start_keyboard())


@router.message(Command('random'))
async def random_handler(message: Message):
    await message.answer('Вот твой рандомный факт')
    fact = await get_fact()
    await message.answer(f"Факт-{fact}")

@router.message(Command('gpt'))
async def gpt_handler(message: Message, state: FSMContext):  # Изменил имя и добавил state
    await message.answer('Что интересует?')
    await state.set_state(GPTDialog.message)

@router.message(GPTDialog.message)
async def gpt_message_handler(message: Message, state: FSMContext):
    await state.clear()
    text = await dialog_gpt_func(message.text)
    await message.answer(f"{text}")

@router.message(Command('quiz'))
async def quiz_handler(message: Message):
    await message.answer('Выбери тему для квиза!', reply_markup=topic_keyboard())

@router.message(Command('talk'))
async def talk_handler(message: Message, state: FSMContext):  # Добавил state
    await message.answer('С кем хочешь поговорить?', reply_markup=persons_keyboard())
    await state.set_state(Talk.persona)






