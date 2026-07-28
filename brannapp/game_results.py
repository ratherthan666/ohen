# pylint: disable=C0301

"""Module for game results"""
from random import randint
from kivy.uix.screenmanager import Screen
from kivy.uix import button, label, textinput, checkbox
from kivy.core.window import Window
from game_status import BranGameStatus

TEXT_SIZE_MODIFIER = {
    "Restart": .025,
    "Score": .05,
    "Winner": .0225,
    "Looser": .0225
}
"""Relative font sizes"""


EVENTS = {
    "Doběh": .70,
    "Spálení": .64,
    "Přešlap": .58,
    "Chybějící pálkař": .52,
    "Homerun": .46,
    "Chycení do jedné ruky": .40,
    "Chycení do obou rukou": .34,
    "Hádka s rozhodčím": .28
}

class GameResults(Screen):
    def __init__(self, app, reseter, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.res_status = app.status
        self.reseter = reseter
        self.components = {}
        self.events = [{}, {}]
        self._setup_ui()
        for comp in self.components.items():
            self.add_widget(comp[1])

    def load_stats(self):
        if self.res_status.score[0] < self.res_status.score[1]:
            self.res_status.switch_sides()

        with open(self.res_status.output) as f:
            df = f.read().split("\n")

        for e in df:
            if e[0] == "č":
                continue
            desc = e.split(",")
            i = self.res_status.team_names.index(desc[1])
            if desc[3] in self.events[i]:
                self.events[i][desc[3]] = self.events[i][desc[3]] + 1
            else:
                self.events[i][desc[3]] = 1

    def reset(self, *_):
        self.reseter()
        self.manager.current = "init"

    def on_enter(self, *_):
        """Fill dynamic fields on entering screen"""
        self.status = self.app.status
        self.load_stats()
        self.components["Winner"].text = self.res_status.team_names[0]
        self.components["Looser"].text = self.res_status.team_names[1]
        self.components["Score"].text = f"{str(self.res_status.score[0]):>3s}-{str(self.res_status.score[1]):<3s}"
        for stat in EVENTS.keys():
            if stat in self.events[0]:
                self.components[f"Winner-{stat}"].text = str(self.events[0][stat])
            else:
                self.components[f"Winner-{stat}"].text = "0"
            if stat in self.events[1]:
                self.components[f"Looser-{stat}"].text = str(self.events[1][stat])
            else:
                self.components[f"Looser-{stat}"].text = "0"
        Window.bind(on_resize=self.resize_texts)
        self.resize_texts(None)

    def resize_texts(self, *_):
        """Resize all texts to fit in components"""
        for comp in self.components.items():
            comp[1].font_size = Window.height * TEXT_SIZE_MODIFIER[comp[0]]
        return self

    def _result_line(self, stat: str, y: float):
        self.components[f"Winner-{stat}"] = label.Label(text="",
                                                        pos_hint={"center_x": .2, "y": y},
                                                        size_hint=(.25, .05))
        self.components[f"{stat}"] = label.Label(text=stat,
                                                 pos_hint={"center_x": .5, "y": y},
                                                 size_hint=(.3, .05))
        self.components[f"Looser-{stat}"] = label.Label(text="",
                                                        pos_hint={"center_x": .8, "y": y},
                                                        size_hint=(.25, .05))
        TEXT_SIZE_MODIFIER[f"Winner-{stat}"] = .05
        TEXT_SIZE_MODIFIER[f"{stat}"] = .02
        TEXT_SIZE_MODIFIER[f"Looser-{stat}"] = .05

    def _setup_ui(self):
        self.components["Restart"] = button.Button(text="Resetovat",
                                                   pos_hint={'center_x': .5, 'y': .05},
                                                   size_hint=(0.40, 0.10))
        self.components["Restart"].bind(on_press=self.reset)
        for stat, y in EVENTS.items():
            self._result_line(stat, y)
        self.components["Winner"] = label.Label(text="",
                                                pos_hint={'center_x': .20, 'y': .85},
                                                size_hint=(.25, .0325))
        self.components["Looser"] = label.Label(text="",
                                                pos_hint={'center_x': .80, 'y': .85},
                                                size_hint=(.25, .0325))
        self.components["Score"] = label.Label(text="",
                                               pos_hint={'center_x': .5, 'y': .85},
                                               size_hint=(0.5, 0.15))