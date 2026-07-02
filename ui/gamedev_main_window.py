"""
Главное окно GameDev
"""

import json
from pathlib import Path
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                             QSplitter, QMessageBox, QInputDialog, QPushButton,
                             QApplication, QDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence, QShortcut
from core.storage import VaultStorage
from core.themes import get_theme, get_stylesheet, DEFAULT_THEME
from ui.ribbon import Ribbon
from ui.file_explorer import FileExplorer
from ui.editor import NoteEditor
from ui.status_bar import StatusBar
from ui.graph_widget import GraphWidget, ConnectNotesDialog
from ui.search_panel import SearchPanel
from ui.tags_panel import TagsPanel
from ui.daily_notes_panel import DailyNotesPanel
from ui.daily_note_dialog import DailyNoteDialog
from ui.gamedev_panel import GameDevPanel
from ui.settings_dialog import SettingsDialog


class GameDevMainWindow(QMainWindow):
    def __init__(self, main_window=None, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setWindowTitle("🎮 GameDev Tracker")
        self.resize(1600, 900)
        self.setStyleSheet("background-color: #1a1b26;")
        self.saved_state = None
        self.gamedev_window = None

        # Загрузка текущей темы
        self.config_file = Path(__file__).parent.parent / "config.json"
        self.current_theme_id = self.load_theme()
        self.apply_theme(self.current_theme_id)

        # Отдельный vault для game dev
        vault_path = Path(__file__).parent.parent / "vault_gamedev"
        vault_path.mkdir(exist_ok=True)
        self.storage = VaultStorage(str(vault_path))
        
        self.current_view = "explorer"
        self.current_note = None

        self.init_ui()
        self.init_shortcuts()

    def load_theme(self) -> str:
        """Загружает тему из конфига"""
        try:
            if self.config_file.exists():
                config = json.loads(self.config_file.read_text(encoding='utf-8'))
                return config.get('theme', DEFAULT_THEME)
        except:
            pass
        return DEFAULT_THEME

    def save_theme(self, theme_id: str):
        """Сохраняет тему в конфиг"""
        try:
            config = {'theme': theme_id}
            self.config_file.write_text(json.dumps(config, indent=2), encoding='utf-8')
        except Exception as e:
            print(f"Ошибка сохранения темы: {e}")

    def apply_theme(self, theme_id: str):
        """Применяет тему"""
        theme = get_theme(theme_id)
        stylesheet = get_stylesheet(theme)
        QApplication.instance().setStyleSheet(stylesheet)
        self.current_theme_id = theme_id

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Ribbon
        self.ribbon = Ribbon(self, is_gamedev_window=True)
        self.ribbon.button_clicked.connect(self.on_ribbon_clicked)
        main_layout.addWidget(self.ribbon)
        self.ribbon.set_active("explorer")

        # 2. Левая панель
        self.left_panel = QWidget()
        self.left_panel.setFixedWidth(280)
        self.left_layout = QVBoxLayout(self.left_panel)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(0)

        # Кнопка "Назад"
        back_btn = QPushButton("← Назад к заметкам")
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7aa2f7, stop:1 #bb9af7);
                color: white;
                border: none;
                padding: 10px 16px;
                margin: 12px;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
        """)
        back_btn.clicked.connect(self.go_back)
        self.left_layout.addWidget(back_btn)

        # Кнопка соединения заметок
        connect_btn = QPushButton("🔗 Соединить заметки")
        connect_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        connect_btn.setStyleSheet("""
            QPushButton {
                background-color: #292e42;
                color: #c0caf5;
                border: 1px solid #3b4261;
                padding: 10px 16px;
                margin: 0 12px 12px 12px;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #3b4261;
                color: #bb9af7;
            }
        """)
        connect_btn.clicked.connect(self.on_connect_notes)
        self.left_layout.addWidget(connect_btn)

        # Проводник
        self.explorer = FileExplorer(str(self.storage.vault_path), self)
        self.explorer.file_selected.connect(self.on_file_selected)
        self.explorer.new_note_requested.connect(self.on_new_note)
        self.explorer.rename_requested.connect(self.on_rename_note)
        self.explorer.delete_requested.connect(self.on_delete_note)
        self.explorer.refresh(self.storage)
        self.left_layout.addWidget(self.explorer)

        # Поиск
        self.search_panel = SearchPanel(self.storage, self)
        self.search_panel.note_selected.connect(self.on_file_selected)
        self.search_panel.hide()
        self.left_layout.addWidget(self.search_panel)

        # Теги
        self.tags_panel = TagsPanel(self.storage, self)
        self.tags_panel.tag_selected.connect(self.on_tag_selected)
        self.tags_panel.hide()
        self.left_layout.addWidget(self.tags_panel)

        # Daily
        self.daily_panel = DailyNotesPanel(self.storage, self)
        self.daily_panel.daily_note_requested.connect(self.on_daily_note_requested)
        self.daily_panel.hide()
        self.left_layout.addWidget(self.daily_panel)

        # GameDev панель
        self.gamedev_panel = GameDevPanel(str(self.storage.vault_path), self)
        self.gamedev_panel.hide()
        self.left_layout.addWidget(self.gamedev_panel)

        main_layout.addWidget(self.left_panel)

        # 3. Центральный splitter: РЕДАКТОР + ГРАФ (всегда видны!)
        center_splitter = QSplitter(Qt.Orientation.Horizontal)
        center_splitter.setHandleWidth(1)
        center_splitter.setStyleSheet("QSplitter::handle { background-color: #292e42; }")

        # Редактор
        self.editor = NoteEditor(self)
        self.editor.content_changed.connect(self.on_content_changed)
        self.editor.tab_selected.connect(self.on_file_selected)
        self.editor.note_color_changed.connect(self.on_note_color_changed)
        center_splitter.addWidget(self.editor)

        # Граф
        self.graph = GraphWidget(self.storage, self)
        self.graph.node_clicked.connect(self.on_file_selected)
        center_splitter.addWidget(self.graph)

        center_splitter.setStretchFactor(0, 3)
        center_splitter.setStretchFactor(1, 1)
        center_splitter.setSizes([1000, 400])

        main_layout.addWidget(center_splitter, stretch=1)

        # Status bar
        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)

    def save_state(self):
        """Сохраняет текущее состояние"""
        self.saved_state = {
            'current_note': self.current_note,
            'current_view': self.current_view,
        }

    def restore_state(self):
        """Восстанавливает состояние"""
        if self.saved_state:
            if self.saved_state.get('current_note'):
                self.on_file_selected(self.saved_state['current_note'])
            if self.saved_state.get('current_view'):
                self.on_ribbon_clicked(self.saved_state['current_view'])

    def go_back(self):
        """Вернуться в основное окно"""
        try:
            print(" Возврат к основному окну...")
            self.save_state()
            self.hide()
            if self.main_window:
                from PyQt6.QtCore import QTimer
                QTimer.singleShot(100, self._show_main_window)
        except Exception as e:
            print(f"❌ Ошибка в go_back: {e}")

    def _show_main_window(self):
        """Показывает основное окно"""
        try:
            if self.main_window:
                self.main_window.restore_state()
                self.main_window.show()
                self.main_window.raise_()
                self.main_window.activateWindow()
                print("✅ Основное окно показано")
        except Exception as e:
            print(f"❌ Ошибка в _show_main_window: {e}")

    def showEvent(self, event):
        """Вызывается при показе окна"""
        try:
            super().showEvent(event)
            self.restore_state()
        except Exception as e:
            print(f" Ошибка в showEvent: {e}")

    def init_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+N"), self, self.on_new_note)
        QShortcut(QKeySequence("Ctrl+W"), self, lambda: self.editor.close_current_tab())
        QShortcut(QKeySequence("Ctrl+P"), self, lambda: self.switch_view("search"))
        QShortcut(QKeySequence("Ctrl+D"), self, lambda: self.switch_view("daily"))
        QShortcut(QKeySequence("Ctrl+G"), self, lambda: self.switch_view("gamedev"))
        QShortcut(QKeySequence("Escape"), self, self.go_back)

    def switch_view(self, view_name: str):
        self.on_ribbon_clicked(view_name)

    def on_ribbon_clicked(self, name: str):
        self.explorer.hide()
        self.search_panel.hide()
        self.tags_panel.hide()
        self.daily_panel.hide()
        self.gamedev_panel.hide()

        if name == "explorer":
            self.explorer.show()
            self.editor.show()
            self.graph.show()
        elif name == "search":
            self.search_panel.show()
            self.search_panel.search_input.setFocus()
            self.editor.show()
            self.graph.show()
        elif name == "tags":
            self.tags_panel.show()
            self.tags_panel.refresh()
            self.editor.show()
            self.graph.show()
        elif name == "daily":
            self.daily_panel.show()
            self.daily_panel.refresh_list()
            self.editor.show()
            self.graph.show()
        elif name == "gamedev":
            self.gamedev_panel.show()
            self.editor.show()
            self.graph.show()
        elif name == "graph":
            # Граф всегда виден, просто активируем вкладку
            self.editor.show()
            self.graph.show()

        self.current_view = name

    def on_file_selected(self, filename: str):
        if filename in self.storage.notes:
            note = self.storage.notes[filename]
            self.current_note = filename
            self.editor.set_title(filename)
            self.editor.set_content(note.content)
            self.editor.current_color = note.color or ""
            self.editor.apply_color(note.color or "")
            self.status_bar.update_counts(note.content, filename)
            self.explorer.refresh(self.storage, filename)

    def on_new_note(self):
        title, ok = QInputDialog.getText(self, "Новая заметка", "Название заметки:")
        if ok and title:
            if title in self.storage.notes:
                QMessageBox.warning(self, "Ошибка", f"Заметка '{title}' уже существует")
                return
            self.storage.save_note(title, f"# {title}\n\n")
            self.explorer.refresh(self.storage, title)
            self.graph.update_graph()
            self.on_file_selected(title)

    def on_rename_note(self, old_title: str, new_title: str):
        if new_title in self.storage.notes:
            QMessageBox.warning(self, "Ошибка", f"Заметка '{new_title}' уже существует")
            return
        content = self.storage.notes[old_title].content
        self.storage.delete_note(old_title)
        self.storage.save_note(new_title, content)
        self.explorer.refresh(self.storage)
        self.graph.update_graph()
        if self.current_note == old_title:
            self.on_file_selected(new_title)

    def on_delete_note(self, title: str):
        self.storage.delete_note(title)
        self.explorer.refresh(self.storage)
        self.graph.update_graph()
        if self.current_note == title:
            self.current_note = None
            self.editor.set_content("")
            self.status_bar.update_counts("", None)

    def on_content_changed(self, content: str):
        self.status_bar.update_counts(content, self.current_note)
        if self.current_note:
            current_color = self.editor.current_color
            self.storage.save_note(self.current_note, content, color=current_color)
            self.graph.update_graph()
            self.tags_panel.refresh()

    def on_note_color_changed(self, color: str):
        """Обновление цвета заметки"""
        if self.current_note:
            content = self.editor.get_content()
            self.storage.save_note(self.current_note, content, color=color)
            self.graph.update_graph()
            print(f"🎨 Цвет заметки '{self.current_note}' изменён на {color or 'без цвета'}")

    def on_tag_selected(self, tag_name: str):
        notes = self.storage.get_by_tag(tag_name)
        if notes:
            self.on_file_selected(notes[0].title)

    def on_daily_note_requested(self, date_str: str):
        if date_str in self.storage.notes:
            self.on_file_selected(date_str)
        else:
            dialog = DailyNoteDialog(date_str, self)
            dialog.note_created.connect(self._on_daily_note_created)
            dialog.exec()

    def _on_daily_note_created(self, date_str: str, content: str):
        self.storage.save_note(date_str, content)
        self.explorer.refresh(self.storage, date_str)
        self.graph.update_graph()
        self.daily_panel.refresh_list()
        self.on_file_selected(date_str)

    def on_connect_notes(self):
        if len(self.storage.notes) < 2:
            QMessageBox.warning(self, "Ошибка", "Нужно минимум 2 заметки")
            return
        dialog = ConnectNotesDialog(self.storage, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            from_note, to_note = dialog.get_notes()
            if from_note and to_note and from_note != to_note:
                self.graph.connect_notes(from_note, to_note)
                self.explorer.refresh(self.storage, self.current_note)

    def open_settings(self):
        """Открывает диалог настроек"""
        dialog = SettingsDialog(self.current_theme_id, self)
        dialog.theme_changed.connect(self.on_theme_changed)
        dialog.exec()

    def on_theme_changed(self, new_theme_id: str):
        """Обработка смены темы"""
        self.save_theme(new_theme_id)
        self.apply_theme(new_theme_id)
        QApplication.instance().setStyleSheet(get_stylesheet(get_theme(new_theme_id)))