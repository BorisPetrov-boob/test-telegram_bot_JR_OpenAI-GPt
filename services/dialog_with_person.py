from openai import AsyncOpenAI
from config import OpenAI_KEY
from openai.types.chat import (ChatCompletionSystemMessageParam,
ChatCompletionAssistantMessageParam, ChatCompletionUserMessageParam)

client = AsyncOpenAI(api_key=OpenAI_KEY)


async def get_persona_response(persona: str, user_message: str) -> str:

    system_prompts = {
        'shakespeare': "Ты - Уильям Шекспир. Говори на старинном английском стиле, используя поэтические выражения и метафоры. Ты великий драматург и поэт.",
        'einstein': "Ты - Альберт Эйнштейн. Говори как гениальный физик, используя научные термины и философские размышления. Иногда добавляй юмор.",
        'lermontov': "Ты - Михаил Лермонтов. Говори на великолепном русском языке в поэтическом стиле. Ты романтик с ноткой грусти и философских раздумий."
    }

    system_message = system_prompts.get(persona, "Ты - полезный помощник.")

    response = await client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            ChatCompletionSystemMessageParam(role="system", content=system_message),
            ChatCompletionUserMessageParam(role="user", content=user_message),
            ChatCompletionAssistantMessageParam(role="assistant", content= "Ответь на это в стиле выбранного персонажа.")
       ],
        temperature=0.8,
        max_tokens=500
    )
    return response.choices[0].message.content