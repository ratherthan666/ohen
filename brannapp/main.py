from kivy.app import App
from game import BranballGame
from kivy.uix.screenmanager import ScreenManager


class BranballApp(App):
    def __init__(self):
        super().__init__()
        self.time = {"hours": 0, "minutes": 1, "seconds": 30}
        self.team_names = ["A", "B"]
        self.score = [0, 0]
        self.batter_list = []
        self.branner = []
        self.manager = ScreenManager()

    def build(self):
        self.manager.add_widget(BranballGame(name="Game", **self.time))
        return self.manager


if __name__ == "__main__":
    app = BranballApp()
    app.run()
