"""Class that defines base class for all bank products"""

import datetime
import math
from abc import ABC, abstractmethod
from enum import Enum
from bank_client import BankClient


class BankProductOperation(Enum):
    """Defines operations with bank product"""
    FOUNDED = "Product founded"
    DEPOSIT = "Deposit to a product"
    WITHDRAW = "Withdraw from a product"
    CLOSURE = "Closure of a product"


class InterestStrategy(Enum):
    """Defines different interest strategies and their deltas"""
    ANNUAL = datetime.timedelta(days=365)
    QUARTERLY = datetime.timedelta(days=91.25)
    MONTHLY = datetime.timedelta(days=30.4167)
    WEEKLY = datetime.timedelta(days=7)
    DAILY = datetime.timedelta(days=1)
    HOURLY = datetime.timedelta(hours=1)
    MINUTELY = datetime.timedelta(minutes=1)
    SECONDLY = datetime.timedelta(seconds=1)


class BankProduct(ABC):
    """Represents a generic bank product"""

    def __init__(self, account_num: int, account_owner: BankClient):
        """
        Initializes a bank product
        :param account_num: Account number
        """
        self.balance = 0.0
        self.num = account_num
        self.owner = account_owner
        self.operations = [[datetime.datetime.now(tz=datetime.timezone.utc), BankProductOperation.FOUNDED]]

    def __lt__(self, other):
        """
        Compares two bank products based on their account number
        :param other: second bank product
        :return: true if this product has lower number than other
        """
        if not isinstance(other, BankProduct):
            raise TypeError
        return self.num < other.num

    def amount(self) -> float:
        """
        Returns the current account balance including interest
        :return: Account balance
        """
        return self.balance + self.interest()

    @abstractmethod
    def deposit(self, amount: float) -> float:
        """
        Performs a deposit event
        :param amount: amount of the deposit
        :return: new balance
        """
        pass

    @abstractmethod
    def withdrawal(self, amount: float) -> float:
        """
        Performs a withdrawal event
        :param amount: amount of the withdrawal
        :return: new balance
        """
        pass

    @abstractmethod
    def interest(self) -> float:
        """
        Count interest from current balance
        :return: Interest value
        """
        pass


class BasicAccount(BankProduct, ABC):
    """Represents a basic bank account"""

    def __init__(self, account_num: int, account_owner: BankClient, interest_rate: float, maintenance_rate: float,
                 maintenance_fare: float, tax_rate: float, interest_strategy: InterestStrategy):
        """
        Initializes a basic bank account with specified parameters
        :param account_num: Account number
        :param account_owner: Account owner
        :param interest_rate: Interest rate
        :param maintenance_rate: Maintenance rate
        :param maintenance_fare: Maintenance fare
        :param tax_rate: Tax rate
        :param interest_strategy: Interest strategy
        """
        super().__init__(account_num, account_owner)
        self.interest_rate = interest_rate
        self.maintenance_rate = maintenance_rate
        self.maintenance_fare = maintenance_fare
        self.tax_rate = tax_rate
        self.interest_strategy = interest_strategy

    def copy(self, account_number: int):
        """
        Initializes a basic bank account as a copy of an existing account
        :param account_number: New account number
        """
        return BasicAccount(account_number, self.owner, self.interest_rate, self.maintenance_rate,
                            self.maintenance_fare,self.tax_rate, self.interest_strategy)

    def deposit(self, amount: float) -> float:
        """
        Performs a deposit event
        :param amount: amount of the deposit
        :return: new balance
        """
        self.balance += self.interest()
        self.balance += amount
        self.operations.append([datetime.datetime.now(tz=datetime.timezone.utc), BankProductOperation.DEPOSIT, amount])
        return self.balance

    def withdrawal(self, amount: float) -> float:
        """
        Performs a withdrawal event
        :param amount: amount of the deposit
        :return: new balance
        """
        self.balance += self.interest()
        self.balance -= amount
        self.operations.append([datetime.datetime.now(tz=datetime.timezone.utc), BankProductOperation.DEPOSIT, amount])
        return self.balance

    def interest(self) -> float:
        """Count interest from current balance, includes maintenance and tax"""
        delta = datetime.datetime.now(tz=datetime.timezone.utc)-self.operations[-1][0]
        periods = delta/self.interest_strategy.value
        interest = self.balance*math.e**(self.interest_rate*(1-self.tax_rate) * periods) - self.balance
        maintenance = self.balance * self.maintenance_rate * periods + periods * self.maintenance_fare
        return interest - maintenance


class BasicLoan(BankProduct, ABC):
    """Represents """
