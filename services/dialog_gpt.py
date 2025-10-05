from config import OpenAI_KEY
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

client = AsyncOpenAI(api_key=OpenAI_KEY)


async def dialog_gpt_func(text):
    response = await client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            ChatCompletionSystemMessageParam(role="system",
                                             content="Ты интересный собеседник, поддерживающий разговор на любые темы"),
            ChatCompletionUserMessageParam(role="user", content=text)
        ],

        temperature=0.7,
        max_tokens=400
    )
    return response.choices[0].message.content
