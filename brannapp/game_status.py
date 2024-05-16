from datetime import datetime


PHASES = ["init", "start", "1st half", "halftime", "2nd half", "results"]
SCREENS = ["init", "halftime", "game", "halftime", "game", "game"]


class BranGameStatus:
    """Game status for Bränball game"""
    def __init__(self):
        self.time = {"hours": 0, "minutes": 0, "seconds": 0}
        self.team_names = ["A", "B"]
        self.score = [0, 0]
        self.batter_list = []
        self.branner = "Bränner"
        self.output = "/storage/emulated/0/Documents/Bran/" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".csv"
        self.ph = 0

    def __next__(self) -> str:
        self.ph += 1
        if self.phase == len(PHASES):
            self.ph = 0
        return SCREENS[self.ph]

    @property
    def phase(self):
        return PHASES[self.ph]

    def switch_sides(self):
        self.team_names = [self.team_names[1], self.team_names[0]]
        self.score = [self.score[1], self.score[0]]
