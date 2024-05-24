from kivy.app import App
from connect_gui import Connection
from kivy.uix.screenmanager import ScreenManager


class BranballApp(App):
    def __init__(self, client: list):
        super().__init__()
        self.client = client
        self.manager = ScreenManager()

    def build(self):
        self.manager.add_widget(Connection(self.client, name="init"))
        self.manager.current = "init"
        return self.manager


if __name__ == "__main__":
    cl = []
    app = BranballApp(cl)
    app.run()
    if cl:
        cl[0].send_exit()
