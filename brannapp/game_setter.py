from random import randint
from kivy.uix.screenmanager import Screen
from kivy.uix import button, label, textinput, checkbox
from kivy.core.window import Window

TEXT_SIZE_MODIFIER = {
    "Time label": .0225,
    "Hours": .04,
    "Minutes": .04,
    "Seconds": .04,
    "Dot1": .05,
    "Dot2": .05,
    "Teams": .0225,
    "Team1": .05,
    "Team2": .05,
    "Dot3": .05,
    "Randomize": .05,
    "Randomize text": .0225,
    "Header": .0225,
    "Confirm": .025
}


class GameSetter(Screen):
    def __init__(self, time: list[dict[str, int]], team_names: list[str], **kwargs):
        super(GameSetter, self).__init__(**kwargs)
        self.time: list[dict[str, int]] = time
        self.team_names: list[str] = team_names
        self.components = {}

        self.setup_ui()
        for comp in self.components.keys():
            self.add_widget(self.components[comp])
        Window.bind(on_resize=self.resize_texts)
        self.resize_texts(None)

    def resize_texts(self, *_):
        for comp in self.components.keys():
            self.components[comp].font_size = Window.height * TEXT_SIZE_MODIFIER[comp]
        return self

    def set_page(self, next_page):
        self.root.current = next_page

    def next(self, _):
        self.time[0]["hours"] = int(self.components["Hours"].text if self.components["Hours"].text != "" else 0)
        self.time[0]["minutes"] = int(self.components["Minutes"].text if self.components["Minutes"].text != "" else 0)
        self.time[0]["seconds"] = int(self.components["Seconds"].text if self.components["Seconds"].text != "" else 0)
        if self.components["Randomize"].active and randint(0, 1) == 1:
            self.team_names[1] = self.components["Team1"].text
            self.team_names[0] = self.components["Team2"].text
        else:
            self.team_names[0] = self.components["Team1"].text
            self.team_names[1] = self.components["Team2"].text
        self.manager.current = "start"

    def setup_ui(self):
        self.components["Header"] = label.Label(text="Vyberte základní parametry zápasu:",
                                                pos_hint={'center_x': .5, 'y': .85},
                                                size_hint=(0.40, 0.16))
        self.components["Time label"] = label.Label(text="Zvolte délku poločasu (formát HH:MM:SS):",
                                                    pos_hint={'center_x': .5, 'y': .75},
                                                    size_hint=(0.35, 0.1))
        self.components["Hours"] = textinput.TextInput(input_filter="int",
                                                       pos_hint={'center_x': .3, 'y': .60},
                                                       size_hint=(0.16, 0.16),
                                                       halign="right",
                                                       hint_text="HH")
        self.components["Minutes"] = textinput.TextInput(input_filter="int",
                                                         pos_hint={'center_x': .5, 'y': .60},
                                                         size_hint=(0.16, 0.16),
                                                         halign="right",
                                                         hint_text="MM")
        self.components["Seconds"] = textinput.TextInput(input_filter="int",
                                                         pos_hint={'center_x': .7, 'y': .60},
                                                         size_hint=(0.16, 0.16),
                                                         halign="right",
                                                         hint_text="SS")
        self.components["Dot1"] = label.Label(text=":",
                                              pos_hint={'center_x': .4, 'y': .60},
                                              size_hint=(0.2, 0.16))
        self.components["Dot2"] = label.Label(text=":",
                                              pos_hint={'center_x': .6, 'y': .60},
                                              size_hint=(0.2, 0.16))

        self.components["Teams"] = label.Label(text="Zadejte názvy týmů:",
                                               pos_hint={'center_x': .5, 'y': .45},
                                               size_hint=(0.35, 0.1))
        self.components["Team1"] = textinput.TextInput(pos_hint={'center_x': .2, 'y': .3},
                                                       size_hint=(0.36, 0.16),
                                                       halign="right",
                                                       hint_text="Pole")
        self.components["Team2"] = textinput.TextInput(pos_hint={'center_x': .8, 'y': .3},
                                                       size_hint=(0.36, 0.16),
                                                       halign="left",
                                                       hint_text="Pálka")
        self.components["Dot3"] = label.Label(text="-",
                                              pos_hint={'center_x': .5, 'y': .3},
                                              size_hint=(0.2, 0.16))
        self.components["Randomize"] = checkbox.CheckBox(pos_hint={'center_x': .5, 'y': .20},
                                                         size_hint=(0.16, 0.16))
        self.components["Randomize text"] = label.Label(text="Náhodně zamíchat počáteční strany",
                                                        pos_hint={'center_x': .5, 'y': .15},
                                                        size_hint=(0.40, 0.16))
        self.components["Confirm"] = button.Button(text="Pokračovat",
                                                   pos_hint={'center_x': .5, 'y': .05},
                                                   size_hint=(0.40, 0.10))
        self.components["Confirm"].bind(on_press=self.next)
