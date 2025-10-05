from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def start_keyboard():
    """Главное меню с кнопкой Старт"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚀 Старт")],
            [KeyboardButton(text="🎭 Персонажи"), KeyboardButton(text="❓ Квиз")],
            [KeyboardButton(text="📊 Случайный факт"), KeyboardButton(text="🌤 Погода")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False,  # Клавиатура не скрывается
        input_field_placeholder="Выберите действие..."
    )

