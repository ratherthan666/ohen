import tkinter as tk
from beh.beh_app.beh_client import Client
from datetime import datetime


class ConnectPage(tk.Frame):
    def __init__(self, parent, client: list, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.client = client
        self.components = {}
        self.ip = tk.StringVar(parent)
        self.port = tk.StringVar(parent)
        self.__create_components()

    def button_handler(self, event):
        try:
            ip = self.ip.get()
            num = int(self.port.get())
            cl = Client(ip, num)
            self.client.append(cl)
            self.parent.destroy()
        except ValueError:
            pass
        except ConnectionResetError:
            pass
        except OSError:
            pass

    def __create_components(self):
        self.components["IP Header"] = tk.Label(text="IP adreasa:", font=("Arial", 28))
        self.components["IP"] = tk.Entry(width=15, font=("Arial", 28),
                                         textvariable=self.ip, justify="left")
        self.components["Port Header"] = tk.Label(text="Port:", font=("Arial", 28))
        self.components["Port"] = tk.Entry(width=5, font=("Arial", 28),
                                         textvariable=self.port, justify="left")
        self.components["Confirm"] = tk.Button(text="Odeslat", width=40, height=8, padx=15, pady=5, font=("Arial", 28),
                                              background="light gray")
        self.components['Confirm'].bind("<Button-1>", self.button_handler)
        for c in self.components:
            self.components[c].pack()


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
    """try:
        cl = Client('localhost', 12345)
    except ConnectionRefusedError:
        print("Nepodařilo se připojit k serveru")
    else:"""
    try:
        cl = []
        root = tk.Tk()
        w = ConnectPage(root, cl)
        try:
            root.mainloop()
        except KeyboardInterrupt:
            print("Aplikace násilně ukončena")
        root = tk.Tk()
        w = MainPage(root, cl[0])
        try:
            root.mainloop()
        except KeyboardInterrupt:
            print("Aplikace násilně ukončena")
        if cl:
            cl[0].send_exit()
    except ConnectionResetError:
        pass
