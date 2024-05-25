# pylint: disable=C0301

"""Module for halftime setter"""
from kivy.uix.screenmanager import Screen
from kivy.uix import button, label, textinput
from kivy.core.window import Window
from datetime import datetime

TEXT_SIZE_MODIFIER = {
"Header": .03,
"Number": .05,
"Confirm": .025,
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


    def setup_ui(self):
        """Setup form UI"""
        self.components["Header"] = label.Label(text="Číslo závodníka:",
                                                pos_hint={'center_x': .5, 'y': .85},
                                                size_hint=(0.40, 0.16), markup=True)
        self.components["Number"] = textinput.TextInput(input_filter="int",
                                                      pos_hint={'center_x': .5, 'y': .30},
                                                      size_hint=(0.6, 0.2),
                                                      halign="right",
                                                      hint_text="Číslo")
        self.components["Confirm"] = button.Button(text="Pokračovat",
                                                   pos_hint={'center_x': .5, 'y': .05},
                                                   size_hint=(0.40, 0.10))
        self.components["Confirm"].bind(on_press=self.next)
