from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from beh.beh_app import connect_gui, client_gui


class BranballApp(App):
    def __init__(self, client: list):
        super().__init__()
        self.client = client
        self.manager = ScreenManager()

    def build(self):
        self.manager.add_widget(connect_gui.Connection(self.client, name="init"))
        self.manager.add_widget(client_gui.Beh(self.client, name="beh"))
        self.manager.current = "init"
        return self.manager


if __name__ == "__main__":
    cl = []
    app = BranballApp(cl)
    app.run()
    if cl:
        cl[0].send_exit()
