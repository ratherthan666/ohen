import time


class AccountClosedException(Exception):
    pass


class Account:
    def __init__(self, interest_rate: float, maintenance_charge_rate: float, maintenance_charge: float,
                 deposit_charge: float, withdrawal_charge: float):
        self.maintenance_charge_rate = maintenance_charge_rate
        self.withdrawal_charge = withdrawal_charge
        self.deposit_charge = deposit_charge
        self.interest_rate = interest_rate
        self.maintenance_charge = maintenance_charge
        self.active = True
        self.balance = 0.0
        self.events = {time.time(): "Account founded."}

    def __str__(self):
        if self.active:
            return f"Account balance {self.balance}."
        return f"Account closed."

    def __float__(self):
        return float(self.balance)

    def __iadd__(self, value: float):
        if not self.active:
            raise AccountClosedException
        self.balance += value
        self.events[time.time()] = f"Deposit: {value}."
        if self.deposit_charge > 0:
            self.balance -= self.deposit_charge
            self.events[time.time()] = f"Deposit charge: -{self.deposit_charge}."
        return self

    def __isub__(self, value: float):
        if not self.active:
            raise AccountClosedException
        self.balance -= value
        self.events[time.time()] = f"Withdrawal: -{value}."
        if self.withdrawal_charge > 0:
            self.balance -= self.withdrawal_charge
            self.events[time.time()] = f"Deposit charge: -{self.withdrawal_charge}."
        return self

    def close(self):
        self.events[time.time()] = "Account deleted"

    def capitalize(self):
        maintenance = self.maintenance_charge
        if self.maintenance_charge_rate > 0:
            maintenance += round(self.maintenance_charge_rate*self.balance,2)
        interest = round(self.interest_rate*self.balance,2)
        self.balance += interest-maintenance
        self.events[time.time()] = f"Maintenance charge and interest: {interest-maintenance}."