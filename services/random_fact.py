from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from config import OpenAI_KEY

client = AsyncOpenAI(api_key=OpenAI_KEY)

async def get_fact():

    response = await client.chat.completions.create(
        model='gpt-4o-mini',
        messages = [
    ChatCompletionSystemMessageParam(role="system", content="Ты полезный ассистент, который знает факты"),
    ChatCompletionUserMessageParam(role="user", content="Верни интересный факт!")
]
)

    return response.choices[0].message.content