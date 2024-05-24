"""Module for client actions"""
import socket
from datetime import datetime


class Client:
    """Class representing client for event \"Běh pro klubovnu\"."""
    client_socket: socket.socket = None

    def __init__(self, addr: str, port: int) -> None:
        """
        Initialize a new client
        :param addr: server ip address
        :param port: server port
        :exception ConnectionRefusedError: if this client cannot to server
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((addr, port))

    def send_result(self, racer_number: int, time: datetime) -> None:
        """
        Sends a result of a racer to server
        :param racer_number: number of racer to send a result ofý
        :param time: result time
        """
        mes = str(racer_number) + "|" + str(time) + "@"
        self.client_socket.sendall(mes.encode())

    def send_exit(self) -> None:
        """Sends an exit message to server and closes the socket"""
        mes = "END@"
        self.client_socket.sendall(mes.encode())
        self.client_socket.close()


if __name__ == "__main__":
    server_address = input("Server address: ")
    server_port = int(input("   Server port: "))
    try:
        c = Client(server_address, server_port)
    except ConnectionRefusedError:
        print("Cannot connect to server")
    else:
        while True:
            ex = input(">")
            finish_time = datetime.now()
            if ex == "EXIT":
                c.send_exit()
                break
            try:
                racer = int(ex)
                print(f"Sending racer {racer}.")
                c.send_result(racer, finish_time)
            except ValueError:
                print("Invalid input")
            except KeyboardInterrupt:
                break
