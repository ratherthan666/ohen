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
        self.status = [BranGameStatus(self)]
        self.manager = ScreenManager()

    def build(self):
        self.manager.add_widget(GameSetter(self.status[0], name="init"))
        self.manager.add_widget(HalftimeSetter(self.status[0], name="halftime"))
        self.manager.add_widget(BranballGame(self.status[0], name="game"))
        self.manager.add_widget(GameResults(self.status, self, name="results"))
        self.manager.current = "init"
        return self.manager


if __name__ == "__main__":
    app = BranballApp()
    app.run()
