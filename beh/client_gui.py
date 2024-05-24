import tkinter as tk
from beh.beh_app.beh_client import Client
from datetime import datetime


class MainPage(tk.Frame):
    def __init__(self, parent: tk.Tk, client: Client, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.client = client
        self.components = {}
        self.user_input = tk.StringVar(parent)
        self.__create_components()

    def button_handler(self, event):
        time = datetime.now()
        try:
            num = int(self.user_input.get())
        except ValueError:
            pass
        else:
            self.components['number'].delete(0, tk.END)
            self.client.send_result(num, time)

    def __create_components(self):
        self.components['label'] = tk.Label(text="Číslo závodníka", font=("Arial", 28))
        self.components['number'] = tk.Entry(width=5, font=("Arial", 200),
                                             textvariable=self.user_input, justify="center")
        self.components['number'].bind('<Return>', self.button_handler)
        self.components['button'] = tk.Button(text="Odeslat", width=40, height=8, padx=15, pady=5, font=("Arial", 28),
                                              background="light gray")
        self.components['button'].bind("<Button-1>", self.button_handler)
        for c in self.components:
            self.components[c].pack()


if __name__ == '__main__':
    try:
        cl = Client('localhost', 12345)
    except ConnectionRefusedError:
        print("Nepodařilo se připojit k serveru")
    else:
        root = tk.Tk()
        w = MainPage(root, cl)
        try:
            root.mainloop()
        except KeyboardInterrupt:
            print("Aplikace násilně ukončena")
        cl.send_exit()
