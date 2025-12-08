from openai import OpenAI
from config import config_obj

client = OpenAI(
    base_url= config_obj.base_url,
    api_key= config_obj.api_key,
)

def answer_script(promt: str):
    response = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=[{"role": "user", "content": promt}],
        max_tokens=500
    )

    return response.choices[0].message.content #принт не работает
