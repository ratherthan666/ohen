"""Module for some random utilities"""
from datetime import datetime
import os
from kivy.app import App
from kivy.utils import platform


PHASES = ["init", "start", "1st half", "halftime", "2nd half", "results"]
"""Phases of game"""
SCREENS = ["init", "halftime", "game", "halftime", "game", "results"]
"""Screens showed during phases of game"""

assert len(PHASES) == len(SCREENS)


class BranGameStatus:
    """Game status for Bränball game"""
    def __init__(self, app: App) -> None:
        """Initialize new game"""
        self.time = {"hours": 0, "minutes": 0, "seconds": 0}
        self.team_names = ["A", "B"]
        self.score = [0, 0]
        self.batter_list = []
        self.branner = "Bränner"
        if platform == "android":
            from android.storage import app_storage_path
            if not os.path.exists(app_storage_path()):
                os.makedirs(app_storage_path())
            self.output = (os.path.join(app_storage_path(), datetime.now().strftime("%Y%m%d-%H%M%S") + ".csv"))
            print(app_storage_path())
        else:
            if not os.path.exists(app.user_data_dir):
                os.makedirs(app.user_data_dir)
            self.output = (os.path.join(app.user_data_dir, datetime.now().strftime("%Y%m%d-%H%M%S") + ".csv"))
            print(app.user_data_dir)
        self.ph = 0

    def __next__(self) -> str:
        """
        Move to the next phase
        :return: relevant screen for the new phase
        """
        self.ph += 1
        if self.ph == len(PHASES):
            exit(0)
        return SCREENS[self.ph]

    @property
    def phase(self) -> str:
        """
        Converts phase number to name
        :return: phase name
        """
        return PHASES[self.ph]

    def switch_sides(self) -> None:
        """
        Switch team sides
        """
        self.team_names = [self.team_names[1], self.team_names[0]]
        self.score = [self.score[1], self.score[0]]
