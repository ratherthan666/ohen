from random import randint
import pandas as pd


class BankClient:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __str__(self):
        return f"{self.kwargs.get('name')} {self.kwargs.get('surname')} ({self.kwargs.get('cuid')})"


class ClientData:
    __CLIENT_NUM_LENGTH = 4

    def __init__(self):
        self.__data = pd.read_csv('clients.csv')

    def data(self) -> pd.DataFrame:
        return pd.DataFrame(self.__data)

    def save(self) -> None:
        self.__data.to_csv('clients.csv', index=False)

    def get_client(self, client_id: int) -> BankClient:
        dl = self.__data[self.__data["cuid"]==client_id].to_dict()
        return BankClient(**{l: str(dl[l][dl[l].keys[0]]) for l in dl})

    def add_client(self) -> int:
        cuid = randint(10**(self.__CLIENT_NUM_LENGTH-1), 10**self.__CLIENT_NUM_LENGTH-1)
        while cuid in set(self.__data["cuid"]):
            cuid = randint(10**(self.__CLIENT_NUM_LENGTH-1), 10**self.__CLIENT_NUM_LENGTH-1)
        dl = {"cuid": cuid}
        for c in list(self.__data.columns)[1:]:
            dl[c] = input(f"Zadejte {c}: ")
        self.__data = self.__data._append(dl, ignore_index=True)
        self.save()
        return cuid
