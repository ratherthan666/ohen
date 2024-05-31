# pylint: disable=C0301

"""Module for halftime setter"""
from kivy.uix.screenmanager import Screen
from kivy.uix import button, label, textinput
from kivy.core.window import Window
from datetime import datetime

TEXT_SIZE_MODIFIER = {
    "Header": .03,
    "Number": .1,
    "Confirm": .05,
    "Cancel": .05,
    "1": .1,
    "2": .1,
    "3": .1,
    "4": .1,
    "5": .1,
    "6": .1,
    "7": .1,
    "8": .1,
    "9": .1
}
"""Relative font sizes"""


class Beh(Screen):
    """Screen for setting variables relevant for whole games"""
    def __init__(self, client: list, **kwargs):
        """
        Initialize screen
        :param status: Game status to fill in
        :param kwargs: arguments to pass in screen constructor
        """
        super().__init__(**kwargs)
        self.client = client
        self.components = {}

        self.setup_ui()
        for comp in self.components.items():
            self.add_widget(comp[1])
        Window.bind(on_resize=self.resize_texts)
        self.resize_texts(None)

    def resize_texts(self, *_):
        """Resize all texts to fit in components"""
        for comp in self.components.items():
            comp[1].font_size = Window.height * TEXT_SIZE_MODIFIER[comp[0]]
        return self

    def next(self, _):
        """Save data from form and go to next screen"""
        time = datetime.now()
        try:
            if self.components["Number"].text != "":
                num = int(self.components["Number"].text)
            else:
                raise ValueError
        except ValueError:
            pass
        else:
            self.components['Number'].text = ""
            self.client[0].send_result(num, time)

    def add_number(self, sender):
        self.components['Number'].text = self.components['Number'].text + sender.text

    def cancel(self, _):
        self.components['Number'].text = ""

    def setup_ui(self):
        """Setup form UI"""
        self.components["Header"] = label.Label(text="Číslo závodníka:",
                                                pos_hint={'center_x': .5, 'y': .85},
                                                size_hint=(0.40, 0.16), markup=True)
        self.components["Number"] = textinput.TextInput(input_filter="int",
                                                        pos_hint={'center_x': .5, 'y': .70},
                                                        size_hint=(0.75, 0.15),
                                                        halign="center")
        self.components["7"] = button.Button(text="7",
                                             pos_hint={'center_x': .25, 'y': .55},
                                             size_hint=(0.25, 0.15))
        self.components["8"] = button.Button(text="8",
                                             pos_hint={'center_x': .5, 'y': .55},
                                             size_hint=(0.25, 0.15))
        self.components["9"] = button.Button(text="9",
                                             pos_hint={'center_x': .75, 'y': .55},
                                             size_hint=(0.25, 0.15))
        self.components["4"] = button.Button(text="4",
                                             pos_hint={'center_x': .25, 'y': .4},
                                             size_hint=(0.25, 0.15))
        self.components["5"] = button.Button(text="5",
                                             pos_hint={'center_x': .5, 'y': .4},
                                             size_hint=(0.25, 0.15))
        self.components["6"] = button.Button(text="6",
                                             pos_hint={'center_x': .75, 'y': .4},
                                             size_hint=(0.25, 0.15))
        self.components["1"] = button.Button(text="1",
                                             pos_hint={'center_x': .25, 'y': .25},
                                             size_hint=(0.25, 0.15))
        self.components["2"] = button.Button(text="2",
                                             pos_hint={'center_x': .5, 'y': .25},
                                             size_hint=(0.25, 0.15))
        self.components["3"] = button.Button(text="3",
                                             pos_hint={'center_x': .75, 'y': .25},
                                             size_hint=(0.25, 0.15))
        for i in range(1, 10):
            self.components[f"{i}"].bind(on_press=self.add_number)
        self.components["Confirm"] = button.Button(text="Odeslat",
                                                   pos_hint={'center_x': .6875, 'y': .1},
                                                   size_hint=(0.375, 0.15))
        self.components["Cancel"] = button.Button(text="Zrušit",
                                                  pos_hint={'center_x': .3125, 'y': .1},
                                                  size_hint=(0.375, 0.15))
        self.components["Confirm"].bind(on_press=self.next)
        self.components["Cancel"].bind(on_press=self.cancel)
