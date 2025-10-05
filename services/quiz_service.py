from config import OpenAI_KEY
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam
import logging

client = AsyncOpenAI(api_key=OpenAI_KEY)

async def get_quiz_question(topic: str) -> str:
    try:
        response = await client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                ChatCompletionSystemMessageParam(
                    role='system',
                    content=f"Сгенерируй один интересный вопрос по теме {topic}"
                ),
                ChatCompletionUserMessageParam(
                    role='user',
                    content=f'Сгенерируй вопрос по теме: {topic}'
                )
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error generating question: {e}")
        return f"Ошибка при генерации вопроса: {e}"

async def check_answer(question: str, answer: str) -> str:
    try:
        response = await client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                ChatCompletionSystemMessageParam(
                    role='system',
                    content='Ты проверяющий ответ на вопрос викторины. Проверь правильность ответа и дай краткий фидбэк.'
                ),
                ChatCompletionUserMessageParam(
                    role='user',
                    content=f'Вопрос: {question}\nОтвет пользователя: {answer}\n\nПравильно ли ответил пользователь?'
                )
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error checking answer: {e}")
        return f"Ошибка при проверке ответа: {e}"