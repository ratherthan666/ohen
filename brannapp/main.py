from kivy.app import App
from game import BranballGame
from game_setter import GameSetter
from kivy.uix.screenmanager import ScreenManager
from datetime import datetime


class BranballApp(App):
    def __init__(self):
        super().__init__()
        self.time = {"hours": 0, "minutes": 0, "seconds": 0}
        self.team_names = ["A", "B"]
        self.score = [0, 0]
        self.batter_list = []
        self.branner = []
        self.output = "/storage/emulated/0/Documents/Bran/" + datetime.now().strftime("%Y%m%d-%H%M%S")
        self.manager = ScreenManager()

    def build(self):
        self.manager.add_widget(GameSetter(team_names=self.team_names, time=[self.time],
                                           name="Setter"))
        self.manager.add_widget(BranballGame(team_names=self.team_names, score_array=self.score,
                                             output_file=[self.output],
                                             # batting_order=self.batter_list,  # branner_name=self.branner,
                                             name="Game", time=[self.time]))
        self.manager.current = "Setter"
        return self.manager


if __name__ == "__main__":
    app = BranballApp()
    app.run()
