from kivy.uix.screenmanager import Screen
from kivy.uix import button, label, textinput
from kivy.core.window import Window
from stopwatch import Stopwatch

TEXT_SIZE_MODIFIER = {
    "Timer button": .02,
    "Timer": .1,
    "Score": .05,
    "Field team": .0225,
    "Branner": .0225,
    "Bran": .02,
    "Circle overstep": .015,
    "Bat team": .0225,
    "Batter number": .05,
    "Batter": .0225,
    "Bat throw": .015,
    "Overstep": .02,
    "Missing batter": .015,
    "Homerun": .02,
    "One hand": .015,
    "Both hands": .015,
    "Fielders argue": .0125,
    "Run-out": .015,
    "Burned": .015,
    "Batters argue": .0125,
    "Backlog": .0125,
    "End": .02
}


class BranballGame(Screen):
    def __init__(self, *, batting_order: list = ["Pálkař"], branner_name: str = "Bränner",
                 score_array: list = [0, 0], output_file: str = None,
                 team_names: list[str] = ["A", "B"], next_page: str = "Game",
                 name: str, **kwargs):
        super().__init__()
        self.batting_order = batting_order
        self.teams = team_names
        self.score_array = score_array
        self.output_file = output_file
        self.batting_index = 0
        self.components = {}
        self.timer = None

        # Setup UI
        self.setup_header(next_page)
        self.setup_branner(branner_name)
        self.setup_bater()
        self.setup_fielder()
        self.setup_runner()

        # Add widgets and bind resize function
        for comp in self.components.keys():
            self.add_widget(self.components[comp])

        Window.bind(on_resize=self.resize_texts)

        self.timer = Stopwatch(out_function=self.display_time, **kwargs)

    def resize_texts(self, *_):
        for comp in self.components.keys():
            self.components[comp].font_size = Window.height * TEXT_SIZE_MODIFIER[comp]
        return self

    def display_time(self, time: str) -> None:
        self.components["Timer"].text = time

    def set_page(self, next_page):
        self.root.current = next_page

    def change_timer(self, _):
        if self.timer.paused:
            self.timer.start()
        else:
            self.timer.stop()

    def make_event(self, team: str, player: str, event: str, points: int):
        if team == self.teams[0] and points > 0:
            self.score_array[0] += points
        elif team == self.teams[0]:
            self.score_array[1] -= points
        elif team == self.teams[1] and points > 0:
            self.score_array[1] += points
        else:
            self.score_array[0] -= points
        self.components["Score"].text = f"{str(self.score_array[0]):>3s}-{str(self.score_array[1]):<3s}"
        str_event = f"\n{self.timer},{team},{player},{event},{points}"
        self.components["Backlog"].text += str_event
        if self.output_file is not None:
            with open(self.output_file, 'a') as f:
                f.write(str_event)
        if event in {"Chycení do jedné ruky", "Chycení do obou rukou", "Brän"}:
            self.batting_index += 1
            if self.batting_index >= len(self.batting_order):
                self.batting_index = 0
            self.components["Batter number"].text = str(self.batting_index)
            self.components["Batter"].text = self.batting_order[self.batting_index]

    def setup_header(self, next_page: str):
        self.components["Timer button"] = button.Button(text="Spustit/zastavit čas",
                                                        pos_hint={'center_x': .5, 'y': .94},
                                                        size_hint=(0.35, 0.05))
        self.components["Timer button"].bind(on_press=self.change_timer)
        self.components["Timer"] = label.Label(text="12:00",
                                               pos_hint={'center_x': .5, 'y': .79},
                                               size_hint=(0.5, 0.15))
        self.components["Score"] = label.Label(text=f"{str(self.score_array[0]):>3s}-{str(self.score_array[1]):<3s}",
                                               pos_hint={'center_x': .5, 'y': .64},
                                               size_hint=(0.5, 0.15))
        self.components["Backlog"] = textinput.TextInput(text="čas,tým,hráč,událost,body",
                                                         pos_hint={'center_x': .5, 'y': .1},
                                                         size_hint=(.3, .5),
                                                         readonly=True,
                                                         halign='left')
        self.components["End"] = button.Button(text="Ukončit",
                                               pos_hint={'center_x': .5, 'y': .02},
                                               size_hint=(0.35, 0.05))
        self.components["Timer button"].bind(on_press=lambda: self.set_page(next_page))

    def setup_branner(self, branner_name: str):
        self.components["Field team"] = label.Label(text=self.teams[0],
                                                    pos_hint={'center_x': .20, 'y': .70},
                                                    size_hint=(.25, .0325))
        self.components["Branner"] = label.Label(text=branner_name,
                                                 pos_hint={'center_x': .20, 'y': .64},
                                                 size_hint=(.25, .0325))
        self.components["Bran"] = button.Button(text="BRÄN",
                                                pos_hint={'center_x': .20, 'y': .55},
                                                size_hint=(.25, .05))
        self.components["Bran"].bind(on_press=lambda _: self.make_event(self.teams[0], branner_name,
                                                                        'Brän', 0))
        self.components["Circle overstep"] = button.Button(text="Překročení kruhu",
                                                           pos_hint={'center_x': .20, 'y': .49},
                                                           size_hint=(.25, .05))
        self.components["Circle overstep"].bind(on_press=lambda _: self.make_event(self.teams[0], branner_name,
                                                                                   'Překročení kruhu', -4))

    def setup_bater(self):
        self.components["Bat team"] = label.Label(text=self.teams[1],
                                                  pos_hint={'center_x': .80, 'y': .70},
                                                  size_hint=(.25, .0325))
        self.components["Batter number"] = label.Label(text=str(self.batting_index+1),
                                                       pos_hint={'center_x': .80, 'y': .65},
                                                       size_hint=(.25, .0325))
        self.components["Batter"] = label.Label(text=self.batting_order[self.batting_index],
                                                pos_hint={'center_x': .80, 'y': .60},
                                                size_hint=(.25, .0325))
        self.components["Bat throw"] = button.Button(text="Odhození pálky",
                                                     pos_hint={'center_x': .80, 'y': .55},
                                                     size_hint=(.25, .05))
        self.components["Bat throw"].bind(on_press=lambda _:
                                          self.make_event(self.teams[1], self.batting_order[self.batting_index],
                                                    'Odhození pálky', -4))
        self.components["Overstep"] = button.Button(text="Přešlap",
                                                    pos_hint={'center_x': .80, 'y': .49},
                                                    size_hint=(.25, .05))
        self.components["Overstep"].bind(on_press=lambda _:
                                         self.make_event(self.teams[1], self.batting_order[self.batting_index],
                                                         'Přešlap', -4))
        self.components["Missing batter"] = button.Button(text="Chybějící pálkař",
                                                          pos_hint={'center_x': .80, 'y': .43},
                                                          size_hint=(.25, .05))
        self.components["Missing batter"].bind(on_press=lambda _:
                                               self.make_event(self.teams[1], self.batting_order[self.batting_index],
                                                         'Chybějící pálkař', -6))
        self.components["Homerun"] = button.Button(text="Homerun",
                                                   pos_hint={'center_x': .80, 'y': .37},
                                                   size_hint=(.25, .05))
        self.components["Homerun"].bind(on_press=lambda _:
                                        self.make_event(self.teams[1], self.batting_order[self.batting_index],
                                                  'Homerun', 6))

    def setup_fielder(self):
        self.components["One hand"] = button.Button(text="Jednou rukou",
                                                    pos_hint={'center_x': .20, 'y': .25},
                                                    size_hint=(.25, .05))
        self.components["One hand"].bind(on_press=lambda _: self.make_event(self.teams[0], "",
                                                                            'Chycení do jedné ruky', 1))
        self.components["Both hands"] = button.Button(text="Oběma rukama",
                                                           pos_hint={'center_x': .20, 'y': .19},
                                                           size_hint=(.25, .05))
        self.components["Both hands"].bind(on_press=lambda _: self.make_event(self.teams[0], "",
                                                                              'Chycení do obou rukou', 2))
        self.components["Fielders argue"] = button.Button(text="Hádka s rozhodčím",
                                                          pos_hint={'center_x': .20, 'y': .13},
                                                          size_hint=(.25, .05))
        self.components["Fielders argue"].bind(on_press=lambda _: self.make_event(self.teams[0], "",
                                                                                  'Hádka s rozhodčím', -6))

    def setup_runner(self):
        self.components["Run-out"] = button.Button(text="Doběh",
                                                   pos_hint={'center_x': .80, 'y': .25},
                                                   size_hint=(.25, .05))
        self.components["Run-out"].bind(on_press=lambda _: self.make_event(self.teams[1], "",
                                                                            'Doběh', 1))
        self.components["Burned"] = button.Button(text="Spálení",
                                                  pos_hint={'center_x': .80, 'y': .19},
                                                  size_hint=(.25, .05))
        self.components["Burned"].bind(on_press=lambda _: self.make_event(self.teams[1], "",
                                                                          'Spálení', -1))
        self.components["Batters argue"] = button.Button(text="Hádka s rozhodčím",
                                                         pos_hint={'center_x': .80, 'y': .13},
                                                         size_hint=(.25, .05))
        self.components["Batters argue"].bind(on_press=lambda _: self.make_event(self.teams[1], "",
                                                                                 'Hádka s rozhodčím', -6))
