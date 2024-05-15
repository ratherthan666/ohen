from kivy.app import App
from game import BranballGame
from game_setter import GameSetter
from halftime_setter import HalftimeSetter
from kivy.uix.screenmanager import ScreenManager
from datetime import datetime


class BranballApp(App):
    def __init__(self):
        super().__init__()
        self.time = {"hours": 0, "minutes": 0, "seconds": 0}
        self.team_names = ["A", "B"]
        self.score = [0, 0]
        self.batter_list = []
        self.branner = ["Bränner"]
        self.output = "/storage/emulated/0/Documents/Bran/" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".csv"
        self.manager = ScreenManager()

    def build(self):
        self.manager.add_widget(GameSetter(team_names=self.team_names, time=[self.time],
                                           name="setter"))
        self.manager.add_widget(HalftimeSetter(name="start", team_names=self.team_names, branner_name=self.branner,
                                               bat_order=self.batter_list, second=False, score=self.score))
        self.manager.add_widget(HalftimeSetter(name="halftime", team_names=self.team_names, branner_name=self.branner,
                                               bat_order=self.batter_list, score=self.score, second=True))
        self.manager.add_widget(BranballGame(team_names=self.team_names, score_array=self.score,
                                             output_file=[self.output],
                                             batting_order=self.batter_list, branner_name=self.branner,
                                             next_page="halftime",
                                             name="game1", time=[self.time]))
        self.manager.add_widget(BranballGame(team_names=self.team_names, score_array=self.score,
                                             output_file=[self.output],
                                             batting_order=self.batter_list,  branner_name=self.branner,
                                             next_page="game2",
                                             name="game2", time=[self.time]))
        self.manager.current = "setter"
        return self.manager


if __name__ == "__main__":
    app = BranballApp()
    app.run()
