
from storage import dialogues, PERSONS
from openai import AsyncOpenAI
from config import OpenAI_KEY
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

client = AsyncOpenAI(api_key=OpenAI_KEY)



async def ask_role_gpt(user_id: int, text: str) -> str:
    print(dialogues[user_id])

    if user_id not in dialogues:
        return 'Сначала начни командой /talk'

    dialogues[user_id]['messages'].append({'role': 'user', 'content': text})

    persona = dialogues[user_id]['persona']

    response = await client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            ChatCompletionSystemMessageParam(role="system", content= f"Ты общаешься в стиле персонажа {persona}"),
            *dialogues[user_id]['messages']
        ]
    )

    return response.choices[0].message.content

