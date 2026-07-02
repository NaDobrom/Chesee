"""
Профессиональная панель разработки игры
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QProgressBar, QInputDialog, QFrame,
                             QScrollArea, QMessageBox, QListWidget, QListWidgetItem)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QLinearGradient, QColor
import json
from pathlib import Path


class TaskItem(QWidget):
    """Карточка задачи"""

    def __init__(self, title: str, completed: bool = False, parent=None):
        super().__init__(parent)
        self.completed = completed
        self.parent_feature = None

        self.setStyleSheet("""
            QWidget {
                background-color: #1e293b;
                border-radius: 10px;
                padding: 4px;
            }
            QWidget:hover {
                background-color: #334155;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(14)

        # Чекбокс (круглый)
        self.checkbox = QPushButton("○" if not completed else "●")
        self.checkbox.setFixedSize(26, 26)
        self.checkbox.setCursor(Qt.CursorShape.PointingHandCursor)
        self.checkbox.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #3b82f6;
                border: 2px solid #3b82f6;
                border-radius: 13px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3b82f6;
                color: white;
            }
        """)
        self.checkbox.clicked.connect(self.toggle_completed)
        layout.addWidget(self.checkbox)

        # Название задачи
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(f"""
            QLabel {{
                color: {'#64748b' if completed else '#e2e8f0'};
                font-size: 13px;
                font-weight: {'400' if completed else '500'};
            }}
        """)
        layout.addWidget(self.title_label, stretch=1)

        # Кнопка удаления
        delete_btn = QPushButton("×")
        delete_btn.setFixedSize(24, 24)
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.setToolTip("Удалить задачу")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #64748b;
                border: none;
                border-radius: 6px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ef4444;
                color: white;
            }
        """)
        delete_btn.clicked.connect(self.delete_task)
        layout.addWidget(delete_btn)

    def toggle_completed(self):
        self.completed = not self.completed
        self.checkbox.setText("●" if self.completed else "○")
        self.title_label.setStyleSheet(f"""
            QLabel {{
                color: {'#64748b' if self.completed else '#e2e8f0'};
                font-size: 13px;
                font-weight: {'400' if self.completed else '500'};
            }}
        """)
        if self.parent_feature:
            self.parent_feature.update_progress()

    def delete_task(self):
        reply = QMessageBox.question(
            self, "Удалить задачу",
            f"Удалить '{self.title_label.text()}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.setParent(None)
            self.deleteLater()
            if self.parent_feature:
                self.parent_feature.update_progress()

    def get_data(self):
        return {"title": self.title_label.text(), "completed": self.completed}


class FeatureCard(QFrame):
    """Карточка фичи с прогрессом"""

    def __init__(self, title: str, description: str = "", progress: int = 0, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1e293b, stop:1 #0f172a);
                border: 1px solid #334155;
                border-radius: 14px;
                padding: 20px;
            }
            QFrame:hover {
                border: 1px solid #3b82f6;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        # Шапка
        header = QHBoxLayout()
        self.title_label = QLabel(f"🎮 {title}")
        self.title_label.setStyleSheet("""
            QLabel {
                color: #f1f5f9;
                font-size: 16px;
                font-weight: 600;
                background: transparent;
            }
        """)
        header.addWidget(self.title_label)

        # Процент
        self.progress_label = QLabel(f"{progress}%")
        self.progress_label.setStyleSheet("""
            QLabel {
                color: #3b82f6;
                font-size: 16px;
                font-weight: bold;
                background: transparent;
            }
        """)
        header.addWidget(self.progress_label)

        # Кнопка удаления
        delete_btn = QPushButton("🗑️")
        delete_btn.setFixedSize(32, 32)
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.setToolTip("Удалить фичу")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #ef4444;
                border: none;
                border-radius: 8px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #ef4444;
                color: white;
            }
        """)
        delete_btn.clicked.connect(self.delete_feature)
        header.addWidget(delete_btn)
        layout.addLayout(header)

        # Описание
        if description:
            desc_label = QLabel(description)
            desc_label.setStyleSheet("""
                QLabel {
                    color: #94a3b8;
                    font-size: 12px;
                    background: transparent;
                }
            """)
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)

        # Прогресс-бар (градиентный)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(progress)
        self.progress_bar.setFormat("")
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #0f172a;
                border: none;
                border-radius: 8px;
                height: 14px;
                text-align: center;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6, stop:0.5 #8b5cf6, stop:1 #ec4899);
                border-radius: 8px;
            }
        """)
        layout.addWidget(self.progress_bar)

        # Контейнер задач
        self.tasks_container = QWidget()
        self.tasks_layout = QVBoxLayout(self.tasks_container)
        self.tasks_layout.setContentsMargins(0, 0, 0, 0)
        self.tasks_layout.setSpacing(10)
        layout.addWidget(self.tasks_container)

        # Кнопка добавления задачи
        add_task_btn = QPushButton("+ Добавить задачу")
        add_task_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_task_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #3b82f6;
                border: 1px dashed #3b82f6;
                padding: 10px;
                border-radius: 8px;
                font-size: 12px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #3b82f6;
                color: white;
                border: 1px solid #3b82f6;
            }
        """)
        add_task_btn.clicked.connect(self.add_task)
        layout.addWidget(add_task_btn)

    def add_task(self):
        title, ok = QInputDialog.getText(self, "Новая задача", "Название задачи:")
        if ok and title:
            task = TaskItem(title, False)
            task.parent_feature = self
            self.tasks_layout.addWidget(task)
            self.update_progress()

    def update_progress(self):
        completed = 0
        total = 0
        for i in range(self.tasks_layout.count()):
            widget = self.tasks_layout.itemAt(i).widget()
            if isinstance(widget, TaskItem):
                total += 1
                if widget.completed:
                    completed += 1
        progress = int((completed / total) * 100) if total > 0 else 0
        self.progress_bar.setValue(progress)
        self.progress_label.setText(f"{progress}%")

        # Обновляем общий прогресс
        parent = self.parent()
        while parent and not hasattr(parent, 'update_total_progress'):
            parent = parent.parent()
        if parent and hasattr(parent, 'update_total_progress'):
            parent.update_total_progress()

    def delete_feature(self):
        title = self.title_label.text().replace("🎮 ", "") if hasattr(self, 'title_label') else "фичу"
        reply = QMessageBox.question(
            self, "Удалить фичу",
            f"Удалить '{title}' со всеми задачами?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            parent_panel = self.parent()
            while parent_panel and not hasattr(parent_panel, 'save_data'):
                parent_panel = parent_panel.parent()

            self.setParent(None)
            self.deleteLater()

            if parent_panel and hasattr(parent_panel, 'save_data'):
                parent_panel.save_data()
                parent_panel.update_total_progress()

    def get_tasks(self):
        tasks = []
        for i in range(self.tasks_layout.count()):
            widget = self.tasks_layout.itemAt(i).widget()
            if isinstance(widget, TaskItem):
                tasks.append(widget.get_data())
        return tasks


class GameDevPanel(QWidget):
    def __init__(self, vault_path, parent=None):
        super().__init__(parent)
        self.vault_path = Path(vault_path)
        self.data_file = self.vault_path / "gamedev_data.json"
        self.setStyleSheet("QWidget { background-color: #0f172a; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Заголовок
        header = QLabel(" GAME DEV")
        header.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6, stop:1 #8b5cf6);
                color: white;
                padding: 14px 20px;
                font-weight: 700;
                font-size: 13px;
                letter-spacing: 1px;
            }
        """)
        layout.addWidget(header)

        # Блок общего прогресса
        progress_container = QWidget()
        progress_container.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1e293b, stop:1 #0f172a);
                border-bottom: 1px solid #334155;
            }
        """)
        progress_layout = QVBoxLayout(progress_container)
        progress_layout.setContentsMargins(20, 20, 20, 20)
        progress_layout.setSpacing(14)

        progress_label = QLabel("📊 Общий прогресс разработки")
        progress_label.setStyleSheet("""
            QLabel {
                color: #94a3b8;
                font-size: 13px;
                font-weight: 500;
                background: transparent;
            }
        """)
        progress_layout.addWidget(progress_label)

        self.total_progress = QProgressBar()
        self.total_progress.setValue(0)
        self.total_progress.setFormat("%p%")
        self.total_progress.setStyleSheet("""
            QProgressBar {
                background-color: #0f172a;
                border: none;
                border-radius: 10px;
                height: 16px;
                text-align: center;
                color: #f1f5f9;
                font-weight: 700;
                font-size: 11px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6, stop:0.5 #8b5cf6, stop:1 #ec4899);
                border-radius: 10px;
            }
        """)
        progress_layout.addWidget(self.total_progress)

        self.progress_percent = QLabel("0%")
        self.progress_percent.setStyleSheet("""
            QLabel {
                color: #3b82f6;
                font-size: 32px;
                font-weight: bold;
                background: transparent;
                padding: 8px 0;
            }
        """)
        self.progress_percent.setAlignment(Qt.AlignmentFlag.AlignCenter)
        progress_layout.addWidget(self.progress_percent)
        layout.addWidget(progress_container)

        # Кнопка добавления фичи (градиентная)
        add_feature_btn = QPushButton("➕ Добавить фичу")
        add_feature_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_feature_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6, stop:1 #8b5cf6);
                color: white;
                border: none;
                padding: 14px;
                margin: 16px;
                border-radius: 10px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2563eb, stop:1 #7c3aed);
            }
            QPushButton:pressed {
                padding-top: 16px;
            }
        """)
        add_feature_btn.clicked.connect(self.add_feature)
        layout.addWidget(add_feature_btn)

        # Скролл-область для фич
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #0f172a;
                width: 10px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #334155;
                min-height: 30px;
                border-radius: 5px;
                margin: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background: #3b82f6;
            }
        """)

        self.features_container = QWidget()
        self.features_layout = QVBoxLayout(self.features_container)
        self.features_layout.setContentsMargins(16, 16, 16, 16)
        self.features_layout.setSpacing(20)
        self.features_layout.addStretch()
        scroll.setWidget(self.features_container)
        layout.addWidget(scroll, stretch=1)

        self.load_data()

    def add_feature(self):
        title, ok = QInputDialog.getText(self, "Новая фича", "Название:")
        if ok and title:
            desc, _ = QInputDialog.getText(self, "Описание", "Описание (необязательно):")
            card = FeatureCard(title, desc or "", 0)
            self.features_layout.insertWidget(self.features_layout.count() - 1, card)
            self.save_data()

    def update_total_progress(self):
        total_tasks = 0
        completed_tasks = 0
        for i in range(self.features_layout.count()):
            widget = self.features_layout.itemAt(i).widget()
            if isinstance(widget, FeatureCard):
                for j in range(widget.tasks_layout.count()):
                    task = widget.tasks_layout.itemAt(j).widget()
                    if isinstance(task, TaskItem):
                        total_tasks += 1
                        if task.completed:
                            completed_tasks += 1
        progress = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0
        self.total_progress.setValue(progress)
        self.progress_percent.setText(f"{progress}%")
        self.save_data()

    def save_data(self):
        data = {"features": [], "total_progress": self.total_progress.value()}
        for i in range(self.features_layout.count()):
            widget = self.features_layout.itemAt(i).widget()
            if isinstance(widget, FeatureCard):
                title = widget.title_label.text().replace("🎮 ", "") if hasattr(widget, 'title_label') else ""
                data["features"].append({
                    "title": title,
                    "progress": widget.progress_bar.value(),
                    "tasks": widget.get_tasks()
                })
        self.data_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')

    def load_data(self):
        if not self.data_file.exists():
            return
        try:
            data = json.loads(self.data_file.read_text(encoding='utf-8'))
            for feature_data in data.get("features", []):
                card = FeatureCard(
                    feature_data.get("title", ""),
                    "",
                    feature_data.get("progress", 0)
                )
                for task_data in feature_data.get("tasks", []):
                    task = TaskItem(
                        task_data.get("title", ""),
                        task_data.get("completed", False)
                    )
                    task.parent_feature = card
                    card.tasks_layout.addWidget(task)
                self.features_layout.insertWidget(self.features_layout.count() - 1, card)
            self.total_progress.setValue(data.get("total_progress", 0))
            self.progress_percent.setText(f"{data.get('total_progress', 0)}%")
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")