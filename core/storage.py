"""
Хранилище данных с поддержкой папок и цветов
"""

import re
import shutil
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from core.models import Note, Tag, DailyNote


class VaultStorage:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.vault_path.mkdir(exist_ok=True)
        self.notes: Dict[str, Note] = {}
        self.tags: Dict[str, Tag] = {}
        self.folders: List[str] = []
        self.load_all_notes()

    def load_all_notes(self):
        self.notes.clear()
        self.tags.clear()
        self.folders.clear()

        for folder in self.vault_path.rglob("*"):
            if folder.is_dir() and folder != self.vault_path:
                rel_path = folder.relative_to(self.vault_path)
                self.folders.append(str(rel_path))

        for md_file in self.vault_path.rglob("*.md"):
            note = self._parse_note(md_file)
            self.notes[note.title] = note
            for tag_name in note.tags:
                if tag_name not in self.tags:
                    self.tags[tag_name] = Tag(name=tag_name)
                self.tags[tag_name].add_note(note.title)

        self._build_backlinks()

    def _parse_note(self, path: Path) -> Note:
        content = path.read_text(encoding='utf-8')
        title = path.stem

        # Извлекаем цвет
        color_match = re.search(r'<!--\s*color:\s*(#[0-9a-fA-F]{6})\s*-->', content)
        color = color_match.group(1) if color_match else ""

        # Убираем цвет из основного контента для редактора
        clean_content = re.sub(r'<!--\s*color:\s*#[0-9a-fA-F]{6}\s*-->\n?', '', content).strip()

        links = set(re.findall(r'\[\[([^\]]+)\]\]', clean_content))
        tags = set()
        for match in re.finditer(r'#([a-zA-Zа-яА-Я0-9_/-]+)', clean_content):
            tag = match.group(1)
            line_start = clean_content.rfind('\n', 0, match.start()) + 1
            line = clean_content[line_start:match.start()]
            if not line.strip().startswith('#'):
                tags.add(tag)

        return Note(
            title=title, path=path, content=clean_content,
            links=links, tags=tags, color=color
        )

    def _build_backlinks(self):
        for note in self.notes.values():
            note.backlinks = set()
        for note in self.notes.values():
            for link in note.links:
                if link in self.notes:
                    self.notes[link].backlinks.add(note.title)

    def save_note(self, title: str, content: str, folder: str = None, color: str = None) -> Note:
        if folder:
            folder_path = self.vault_path / folder
            folder_path.mkdir(parents=True, exist_ok=True)
            path = folder_path / f"{title}.md"
        else:
            path = self.vault_path / f"{title}.md"

        # Сохраняем старый цвет если не передан новый
        old_color = self.notes[title].color if title in self.notes else ""
        final_color = color if color is not None else old_color

        # Формируем контент с мета-тегом цвета
        meta = f"<!-- color: {final_color} -->\n" if final_color else ""
        full_content = meta + content

        path.write_text(full_content, encoding='utf-8')
        note = self._parse_note(path)
        note.updated_at = datetime.now().isoformat()
        self.notes[title] = note

        self._rebuild_tags()
        self._build_backlinks()
        return note

    def delete_note(self, title: str):
        if title in self.notes:
            try:
                self.notes[title].path.unlink()
            except:
                pass
            del self.notes[title]
            self._rebuild_tags()
            self._build_backlinks()

    def create_folder(self, folder_name: str, parent_folder: str = None):
        folder_path = self.vault_path / parent_folder / folder_name if parent_folder else self.vault_path / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)
        self.load_all_notes()

    def delete_folder(self, folder_name: str):
        folder_path = self.vault_path / folder_name
        if folder_path.exists() and folder_path.is_dir():
            for md_file in folder_path.rglob("*.md"):
                note = self._parse_note(md_file)
                if note.title in self.notes: del self.notes[note.title]
            shutil.rmtree(folder_path)
            self.load_all_notes()

    def get_folders(self) -> List[str]:
        return sorted(self.folders)

    def get_notes_in_folder(self, folder: str) -> List[Note]:
        return sorted([self._parse_note(f) for f in (self.vault_path / folder).glob("*.md")], key=lambda n: n.title)

    def _rebuild_tags(self):
        self.tags.clear()
        for note in self.notes.values():
            for tag_name in note.tags:
                if tag_name not in self.tags: self.tags[tag_name] = Tag(name=tag_name)
                self.tags[tag_name].add_note(note.title)

    def search(self, query: str) -> List[Note]:
        q = query.lower()
        return sorted([n for n in self.notes.values() if q in n.title.lower() or q in n.content.lower()],
                      key=lambda n: n.title)

    def get_by_tag(self, tag_name: str) -> List[Note]:
        return [self.notes[t] for t in self.tags[tag_name].notes if t in self.notes] if tag_name in self.tags else []

    def get_all_tags(self) -> List[str]:
        return sorted(self.tags.keys())

    def create_daily_note(self, date: str = None) -> Note:
        date = date or DailyNote.get_today_date()
        path = self.vault_path / f"{date}.md"
        if not path.exists():
            path.write_text(f"# Ежедневная заметка: {date}\n\n## Задачи\n- [ ] \n\n## Заметки\n\n", encoding='utf-8')
        return self._parse_note(path)

    def get_daily_note(self, date: str) -> Optional[Note]:
        return self.notes.get(date)