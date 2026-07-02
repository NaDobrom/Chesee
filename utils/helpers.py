"""
Вспомогательные функции
"""

import markdown
from pathlib import Path


def render_markdown(text: str) -> str:
    """Рендерит Markdown в HTML"""
    extensions = ['fenced_code', 'tables', 'toc', 'nl2br']
    return markdown.markdown(text, extensions=extensions)


def get_file_size(path: Path) -> str:
    """Возвращает размер файла в читаемом формате"""
    size = path.stat().st_size
    if size < 1024:
        return f"{size} B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    else:
        return f"{size / (1024 * 1024):.1f} MB"


def count_words(text: str) -> int:
    """Считает количество слов в тексте"""
    return len(text.split())


def count_chars(text: str) -> int:
    """Считает количество символов в тексте"""
    return len(text)