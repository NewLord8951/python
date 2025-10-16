import os
from mistralai import Mistral
from typing import List, Dict


from dotenv import load_dotenv
load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    raise ValueError("MISTRAL_API_KEY не найден в .env")

client = Mistral(api_key=MISTRAL_API_KEY)

INTRODUCTION_PROMPT = """
На основе этих фактов {facts} напиши введение для студенческого доклада на тему "{topic}".
Объем: 150-200 слов. Стиль: научно-популярный.
"""

SECTION_PROMPT = """
Используя факты {facts}, напиши раздел "{section_title}". 
Объем: 300-400 слов. Структура: тезис - аргументы - вывод.
"""

CONCLUSION_PROMPT = """
Напиши заключение по теме "{topic}", обобщая ключевые идеи. Объем: 150-200 слов.
"""

ABSTRACT_PROMPT = """
Напиши краткую аннотацию (100 слов) к докладу на тему "{topic}".
"""


def generate_text(prompt: str) -> str:
    try:
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Ошибка генерации: {e}")
        return "Ошибка генерации текста."


def generate_introduction(topic: str, facts: List[str]) -> str:
    facts_str = "\n".join(facts[:10])
    prompt = INTRODUCTION_PROMPT.format(facts=facts_str, topic=topic)
    return generate_text(prompt)


def generate_section(section_title: str, facts: List[str]) -> str:
    facts_str = "\n".join(facts)
    prompt = SECTION_PROMPT.format(facts=facts_str, section_title=section_title)
    return generate_text(prompt)


def generate_conclusion(topic: str) -> str:
    prompt = CONCLUSION_PROMPT.format(topic=topic)
    return generate_text(prompt)


def generate_abstract(topic: str) -> str:
    prompt = ABSTRACT_PROMPT.format(topic=topic)
    return generate_text(prompt)
