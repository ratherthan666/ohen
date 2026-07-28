"""
Version: 0.2 Alpha
Release date: 4.11.2024
Author: Robin Palán
"""

from kivy.app import App
from game import BranballGame
from game_setter import GameSetter
from halftime_setter import HalftimeSetter
from kivy.uix.screenmanager import ScreenManager
from game_status import BranGameStatus
from game_results import GameResults


class BranballApp(App):
    def __init__(self):
        super().__init__()
        self.status = BranGameStatus(self)
        self.manager = ScreenManager()

    def _reset(self):
        self.status = BranGameStatus(self)

    def build(self):
        self.manager.add_widget(GameSetter(self, name="init"))
        self.manager.add_widget(HalftimeSetter(self, name="halftime"))
        self.manager.add_widget(BranballGame(self, name="game"))
        self.manager.add_widget(GameResults(self, self._reset, name="results"))
        self.manager.current = "init"
        return self.manager


if __name__ == "__main__":
    app = BranballApp()
    app.run()
