"""
Модели данных
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Set
from datetime import datetime


@dataclass
class Note:
    """Модель заметки"""
    title: str
    path: Path
    content: str
    links: Set[str] = field(default_factory=set)
    tags: Set[str] = field(default_factory=set)
    backlinks: Set[str] = field(default_factory=set)
    color: str = ""  # HEX цвет кружка в графе
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Tag:
    """Модель тега"""
    name: str
    notes: Set[str] = field(default_factory=set)

    def add_note(self, note_title: str):
        self.notes.add(note_title)

    def remove_note(self, note_title: str):
        self.notes.discard(note_title)


@dataclass
class DailyNote:
    """Модель ежедневной заметки"""
    date: str
    content: str = ""

    @staticmethod
    def get_today_date() -> str:
        return datetime.now().strftime("%Y-%m-%d")