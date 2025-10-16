import argparse
import os
from wiki_parser import search_wikipedia, parse_article, extract_key_facts
from content_generator import (
    generate_introduction,
    generate_section,
    generate_conclusion,
    generate_abstract
)
from gost_formatter import (
    Document,
    create_title_page,
    add_table_of_contents,
    add_section,
    add_references,
    set_document_style,
    set_margins,
    save_document
)


def generate_report(topic: str, pages: int = 5) -> str:
    print(f"Генерация доклада по теме: {topic}...")

    topics = [topic, f"{topic} applications", f"{topic} history"]
    urls = search_wikipedia(topics)
    all_text = ""
    for url in urls.values():
        all_text += parse_article(url) + "\n"
    
    if not all_text.strip():
        raise ValueError("Не удалось найти статьи в Wikipedia по теме.")

    facts = extract_key_facts(all_text)

    intro = generate_introduction(topic, facts)
    conclusion = generate_conclusion(topic)
    abstract = generate_abstract(topic)

    sections = {
        "1. Диагностика заболеваний с помощью ИИ": generate_section("Диагностика заболеваний с помощью ИИ", facts),
        "2. Роботизированная хирургия": generate_section("Роботизированная хирургия", facts),
        "3. Персонализированное лечение": generate_section("Персонализированное лечение", facts)
    }

    doc = Document()
    set_document_style(doc)
    set_margins(doc)

    create_title_page(doc, topic)
    add_table_of_contents(doc)

    add_section(doc, "Введение", intro)
    for title, content in sections.items():
        add_section(doc, title, content)
    add_section(doc, "Заключение", conclusion)
    add_references(doc, topic)

    filename = f"report_{topic.replace(' ', '_')}.docx"
    filepath = save_document(doc, filename)
    print(f"Доклад сохранён: {filepath}")
    return filepath


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Генератор учебных работ по ГОСТ")
    parser.add_argument("--topic", type=str, required=True, help="Тема доклада")
    parser.add_argument("--pages", type=int, default=5, help="Желаемый объём (в страницах)")
    args = parser.parse_args()

    generate_report(args.topic, args.pages)
