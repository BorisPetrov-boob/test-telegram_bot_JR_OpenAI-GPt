from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_keyboard():
    kb_list = [
        [InlineKeyboardButton(text='🎲 Интересный факт', callback_data='random_fact')],
        [InlineKeyboardButton(text='🤖 ChatGPT', callback_data='chat_gpt')],
        [InlineKeyboardButton(text='👥 Общение с личностью', callback_data='persona')],
        [InlineKeyboardButton(text='🧠 Quiz', callback_data='quiz')],

    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def fact_again_keyboard():
    kb_list = [
        [InlineKeyboardButton(text='🎲 Хочу еще факт', callback_data='random_fact')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def persons_keyboard():
    kb_list = [
        [InlineKeyboardButton(text='👤 Шекспир', callback_data='shakespeare')],
        [InlineKeyboardButton(text='👤 Эйнштейн', callback_data="einstein")],
        [InlineKeyboardButton(text='👤 Лермонтов', callback_data='lermontov')],

    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def close_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Закрыть", callback_data="close_keyboard")]
        ]
    )


def topic_keyboard():
    kb_list = [
        [InlineKeyboardButton(text='История', callback_data='topic:history')],
        [InlineKeyboardButton(text='Наука', callback_data="topic:science")],
        [InlineKeyboardButton(text="IT", callback_data='topic:it')]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def qviz_answer_keyboard():
    kb_list = [
        [InlineKeyboardButton(text='Еще вопрос', callback_data='next_question')],
        [InlineKeyboardButton(text='Сменить тему', callback_data='change_topic')],
        [InlineKeyboardButton(text='Закончить', callback_data='end_quiz')]

    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard
