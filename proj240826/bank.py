from random import randint
from bank_product import BankClient, BasicAccount, BasicLoan, InterestStrategy


def ask(asking_for: str):
    return input(asking_for)


class MyBasicBank:
    clients = {}
    accounts = {}
    def add_client(self, name, surname):
        cid = randint(100000, 1000000000)
        while cid in self.clients:
            cid = randint(100000, 1000000000)
        self.clients[cid] = (BankClient(cid, name, surname))

    def find_clients(self, *, cid: int=None, name:str=None, surname:str=None):
        for client_id, client in self.clients:
            if ((cid is None or client_id == cid) and (name is None or client.name == name) and
                    (surname is None or client.surname == surname)):
                print(client)

    def new_account(self, cid):
        try:
            cl = self.clients[cid]
        except KeyError:
            print(f"Client {cid} do not exists.")
            return
        account_num = randint(100000, 1000000000)
        while account_num in self.accounts:
            account_num = randint(100000, 1000000000)
        self.accounts[account_num] = BasicAccount(account_num, cl, interest_rate=float(ask('Jaká je úroková sazba?')),
                                                  maintenance_rate=float(ask('Jaká je sazba za vedení účtu (v %)?')),
                                                  maintenance_fare=float(ask('Jaká je pevná sazba za vedení účtu?')),
                                                  tax_rate=float(ask('Jaká je sazba daně z příjmu?')),
                                                  interest_strategy=InterestStrategy.HOURLY)