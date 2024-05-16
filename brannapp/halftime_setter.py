from kivy.uix.screenmanager import Screen
from kivy.uix import button, label, textinput, checkbox
from kivy.core.window import Window
from game_status import BranGameStatus

TEXT_SIZE_MODIFIER = {
    "Header": .0225,
    "Fielders": .0225,
    "Branner": .05,
    "Batters": .0225,
    "Order": .025,
    "Confirm": .025
}


class HalftimeSetter(Screen):
    def __init__(self, status: BranGameStatus, **kwargs):
        super(HalftimeSetter, self).__init__(**kwargs)
        self.status = status
        self.components = {}
        self.setup_ui()
        for comp in self.components.keys():
            self.add_widget(self.components[comp])

    def on_enter(self, *args):
        if self.status.phase == "halftime":
            self.status.switch_sides()
        self.components["Header"].text = (f"Vítejte ve {2 if self.status.phase == 'halftime' else 1}."
                                          f"poločase zápasu.\n"
                                          f"Stav je {str(self.status.score[0]):>3s}-{str(self.status.score[1]):<3s}")
        self.components["Fielders"].text = (f"V poli je tým {self.status.team_names[0]}."
                                            f"\nZadejte jméno brännera:")
        self.components["Batters"].text = (f"Na pálce je tým {self.status.team_names[1]}.\n"
                                           f"Zadejte pořadí pálkařů\nvždy 1 jméno na řádku:")
        self.components["Branner"].text = ""
        self.components["Order"].text = ""
        Window.bind(on_resize=self.resize_texts)
        self.resize_texts(None)

    def resize_texts(self, *_):
        for comp in self.components.keys():
            self.components[comp].font_size = Window.height * TEXT_SIZE_MODIFIER[comp]
        return self

    def next(self, _):
        if self.components["Branner"].text:
            self.status.branner = self.components["Branner"].text
        self.status.batter_list = []
        for k in self.components["Order"].text.split("\n"):
            if k != "":
                self.status.batter_list.append(k)
        if not self.status.batter_list:
            self.status.batter_list = ["Pálkař"]
        self.manager.current = next(self.status)

    def setup_ui(self):
        self.components["Header"] = label.Label(text=f"Vítejte ve {2 if self.status.phase == 'halftime' else 1}. "
                                                     f"poločase zápasu.\n"
                                                     f"Stav je {str(self.status.score[0]):>3s}-{str(self.status.score[1]):<3s}",
                                                pos_hint={'center_x': .5, 'y': .85},
                                                size_hint=(0.40, 0.16))
        self.components["Fielders"] = label.Label(text=f"V poli je tým {self.status.team_names[0]}."
                                                       f"\nZadejte jméno brännera:",
                                                  pos_hint={'center_x': .25, 'y': .75},
                                                  size_hint=(0.40, 0.1))
        self.components["Branner"] = textinput.TextInput(pos_hint={'center_x': .25, 'y': .6},
                                                         size_hint=(0.40, 0.1),
                                                         halign="left",
                                                         hint_text="Branner")
        self.components["Batters"] = label.Label(text=f"Na pálce je tým {self.status.team_names[1]}.\n"
                                                      f"Zadejte pořadí pálkařů\nvždy 1 jméno na řádku:",
                                                 pos_hint={'center_x': .75, 'y': .75},
                                                 size_hint=(0.40, 0.1))
        self.components["Order"] = textinput.TextInput(pos_hint={'center_x': .75, 'y': .2},
                                                       size_hint=(0.40, 0.5),
                                                       halign="left",
                                                       hint_text="Pálkař1\nPálkař2\nPálkař3\n...")
        self.components["Confirm"] = button.Button(text="Pokračovat",
                                                   pos_hint={'center_x': .5, 'y': .05},
                                                   size_hint=(0.40, 0.10))
        self.components["Confirm"].bind(on_press=self.next)
