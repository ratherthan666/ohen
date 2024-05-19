"""Server module for \"Běh pro klubovnu\" event"""
import socket
import threading as th
from datetime import datetime

FILE = "race.csv"
COLORS = {
    'HEADER': '\033[95m',
    'OK_BLUE': '\033[94m',
    'OK_CYAN': '\033[96m',
    'OK_GREEN': '\033[92m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'NORMAL': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m',
}


def time_print() -> str:
    """
    Converts current time to format HH:MM:SS
    :return: converted time
    """
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


def thread_function(client_socket: socket.socket, client_id: int) -> None:
    """
    Thread function that serves one client
    :param client_socket: socket object of client to communicate with
    :param client_id: id for prints
    """
    try:
        print(f"[{time_print()}]:\t{COLORS['OK_BLUE']}Server:\tThread for client"
              f" {client_id} created.{COLORS['NORMAL']}")
        buffer = ""
        end = False
        while True:
            data = client_socket.recv(1024)
            buffer += data.decode()
            while "@" in buffer:
                mes = buffer.split("@")[0]
                buffer = "@".join(buffer.split("@")[1:])
                if mes == "END":
                    end = True
                    break
                row = f'{mes.split("|")[0]},\"{mes.split("|")[1]}\"'
                print(f"[{time_print()}]:\t{COLORS['OK_CYAN']}Client"
                      f" {client_id}:\t{row}{COLORS['NORMAL']}")
                with open(FILE, "a", encoding="utf8") as f:
                    f.write(row+"\n")
            if end:
                print(f"[{time_print()}]:\t{COLORS['OK_BLUE']}Client"
                      f" {client_id}:\tConnection closed.{COLORS['NORMAL']}")
                break
        client_socket.close()
    except ConnectionResetError:
        print(f"[{time_print()}]:\t{COLORS['FAIL']}Client "
              f"{client_id}:\tConnection lost.{COLORS['NORMAL']}")


class Server:
    """Server helper class"""
    server_socket: socket.socket = None

    def __init__(self, address: str, port: int):
        """
        Initialize server
        :param address: IP address of server
        :param port: port on which server is bind
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((address, port))
        print(f"[{time_print()}]:\t{COLORS['OK_GREEN']}Server: "
              f"Server bind on {address}:{port}{COLORS['NORMAL']}")

    def __str__(self):
        return f"\"Běh pro klubovnu\" server bind on {self.server_socket.getsockname()}"

    def start_server(self) -> None:
        """Main server loop, accepting clients"""
        self.server_socket.listen(1)
        thread_id = 1
        threads = []
        try:
            while True:
                print(f"[{time_print()}]:\t{COLORS['OK_BLUE']}Server:\tWaiting{COLORS['NORMAL']}")
                client_socket, client_address = self.server_socket.accept()
                print(f"[{time_print()}]:\t{COLORS['OK_GREEN']}Server:"
                      f"\tConnected to {client_address[0]}:"
                      f"{client_address[1]}{COLORS['NORMAL']}")
                thr = th.Thread(target=thread_function, args=(client_socket, thread_id))
                threads.append(thr)
                thread_id += 1
                thr.start()
        except KeyboardInterrupt:
            # Wait for threads to be finished, prevent the server from accepting new clients
            print(f"[{time_print()}]:\t{COLORS['WARNING']}Server:\tClosing, waiting for "
                  f"all clients to disconnect.{COLORS['NORMAL']}")
            try:
                for thr in threads:
                    thr.join()
                self.server_socket.close()
                print(f"[{time_print()}]:\t{COLORS['OK_GREEN']}Server:\tProperly "
                      f"closed.{COLORS['NORMAL']}")
            except KeyboardInterrupt:
                print(f"[{time_print()}]:\t{COLORS['FAIL']}Server:\tNot closed properly, ghost "
                      f"clients probably remained.{COLORS['NORMAL']}")


if __name__ == "__main__":
    try:
        server_address = input("Server address: ")
        server_port = int(input("   Server port: "))
        s = Server(server_address, server_port)
    except KeyboardInterrupt:
        print("")
        print(f"[{time_print()}]:\t{COLORS['FAIL']}Server:\tNot "
              f"opened.{COLORS['NORMAL']}")
    except socket.gaierror:
        print(f"[{time_print()}]:\t{COLORS['FAIL']}Server:\tCannot "
              f"resolve address.{COLORS['NORMAL']}")
    except ValueError:
        print(f"[{time_print()}]:\t{COLORS['FAIL']}Server:\tInvalid "
              f"port, has to be integer.{COLORS['NORMAL']}")
    except PermissionError:
        print(f"[{time_print()}]:\t{COLORS['FAIL']}Server:\tInvalid "
              f"port, this port is unreachable or do not exists.{COLORS['NORMAL']}")
    except OverflowError:
        print(f"[{time_print()}]:\t{COLORS['FAIL']}Server:\tInvalid "
              f"port, this port is unreachable or do not exists.{COLORS['NORMAL']}")
    else:
        s.start_server()
