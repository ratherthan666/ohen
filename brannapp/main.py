from kivy.app import App
from game import BranballGame
from game_setter import GameSetter
from halftime_setter import HalftimeSetter
from kivy.uix.screenmanager import ScreenManager
from game_status import BranGameStatus


class BranballApp(App):
    def __init__(self):
        super().__init__()
        self.status = BranGameStatus()
        self.manager = ScreenManager()

    def build(self):
        self.manager.add_widget(GameSetter(self.status, name="init"))
        self.manager.add_widget(HalftimeSetter(self.status, name="halftime"))
        self.manager.add_widget(BranballGame(self.status, name="game"))
        self.manager.current = "init"
        return self.manager


if __name__ == "__main__":
    app = BranballApp()
    app.run()
