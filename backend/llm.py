import os
from openai import OpenAI
from pydantic import BaseModel
from typing import Any, Type
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o-mini"

def execute_prompt_with_pydantic(
    template: str,
    data: dict,
    pydantic_model: Type[BaseModel],
    system_prompt: str = None
):
    prompt = template.format(**data)
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.parse(
        model=MODEL,
        messages=messages,
        response_format=pydantic_model,
    )
    return response.choices[0].message.parsed 