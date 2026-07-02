"""
GameDev окно - wrapper для GameDevMainWindow
"""

from PyQt6.QtWidgets import QMainWindow
from ui.gamedev_main_window import GameDevMainWindow


class GameDevWindow(GameDevMainWindow):
    """GameDev окно"""

    def __init__(self, vault_path, parent=None):
        # parent - это основное окно (ObsidianClone)
        super().__init__(main_window=parent)
        # НЕ передаём parent в QMainWindow, чтобы избежать проблем с памятью