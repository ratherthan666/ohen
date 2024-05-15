from kivy.uix.screenmanager import Screen
from kivy.uix import button, label, textinput, checkbox
from kivy.core.window import Window

TEXT_SIZE_MODIFIER = {
    "Header": .0225,
    "Fielders": .0225,
    "Branner": .05,
    "Batters": .0225,
    "Order": .025,
    "Confirm": .025
}


class HalftimeSetter(Screen):
    def __init__(self, team_names: list[str], branner_name: list[str], score: list[int],
                 bat_order: list[str], second: bool = False, **kwargs):
        super(HalftimeSetter, self).__init__(**kwargs)
        self.branner_name = branner_name
        self.team_names = team_names
        self.bat_order = bat_order
        self.score = score
        self.second: bool = second
        self.components = {}

    def on_enter(self, *args):
        if self.second:
            tmp = self.team_names[0]
            self.team_names[0] = self.team_names[1]
            self.team_names[1] = tmp
            tmp = self.score[0]
            self.score[0] = self.score[1]
            self.score[1] = tmp
        self.setup_ui()
        for comp in self.components.keys():
            self.add_widget(self.components[comp])
        Window.bind(on_resize=self.resize_texts)
        self.resize_texts(None)

    def resize_texts(self, *_):
        for comp in self.components.keys():
            self.components[comp].font_size = Window.height * TEXT_SIZE_MODIFIER[comp]
        return self

    def next(self, _):
        if self.components["Branner"].text:
            self.branner_name[0] = self.components["Branner"].text
        while self.bat_order:
            del self.bat_order[-1]
        for k in self.components["Order"].text.split("\n"):
            if k != "":
                self.bat_order.append(k)
        self.manager.current = f"game{2 if self.second else 1}"
        if not self.bat_order:
            self.bat_order.append("Pálkař")

    def setup_ui(self):
        self.components["Header"] = label.Label(text=f"Vítejte ve {2 if self.second else 1}. poločase zápasu.\n"
                                                     f"Stav je {str(self.score[0]):>3s}-{str(self.score[1]):<3s}",
                                                pos_hint={'center_x': .5, 'y': .85},
                                                size_hint=(0.40, 0.16))
        self.components["Fielders"] = label.Label(text=f"V poli je tým {self.team_names[0]}.\nZadejte jméno brännera:",
                                                  pos_hint={'center_x': .25, 'y': .75},
                                                  size_hint=(0.40, 0.1))
        self.components["Branner"] = textinput.TextInput(pos_hint={'center_x': .25, 'y': .6},
                                                         size_hint=(0.40, 0.1),
                                                         halign="left",
                                                         hint_text="Branner")
        self.components["Batters"] = label.Label(text=f"Na pálce je tým {self.team_names[1]}.\n"
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
