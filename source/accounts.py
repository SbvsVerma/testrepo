"""
XYZ
"""

from abc import ABC, abstractmethod
from pickle import dump, load
from time import time


class Account(ABC):
    bank_name = "Void"

    def __init__(self, name, passwd, balance):
        assert balance > 0, "Can't create a account with zero/-ve funds"
        assert len(passwd) >= 8, "Please type a password of 8 or more characters"

        self.balance = balance
        self.__name = name
        self.__passwd = passwd
        self.created_on = time()

    @property
    def name(self):
        return self.__name

    @property
    def passwd(self):
        return None

    @name.setter
    def name(self, new_name):
        assert new_name != self.__name, "Name already in use"

        self.__name = new_name

    @passwd.setter
    def passwd(self, new_passwd):
        assert new_passwd != self.__passwd, "Password already in use"
        assert len(new_passwd) >= 8, "Please type a password of 8 or more characters"

        self.__passwd = new_passwd

    @staticmethod
    def save(acc_obj):
        with open(f"{acc_obj.name}.pkl", "wb") as file:
            dump(acc_obj, file, -1)

    @staticmethod
    def load(acc_name, password):
        try:
            with open(f"{acc_name}.pkl", "rb") as file:
                tmp = load(file)
            if tmp.check_passwd(password):
                return tmp
            raise Exception("Wrong Password!")
        except FileNotFoundError:
            raise FileNotFoundError(
                "Looks like we can't find a account with that name!"
            )

    @abstractmethod
    def withdraw(self, amount):
        assert amount > 0, "Can't withdraw a zero/-ve sum"

        self.balance -= amount

    @abstractmethod
    def deposit(self, amount):
        assert amount > 0, "Can't deposit a zero/-ve sum"

        self.balance += amount

    @abstractmethod
    def apply_interest(self):
        if (time() - self.created_on) >= 31536000:
            self.balance = self.balance + (self.balance * 0)

    def transfer(self, amount, receiver):
        assert amount > 0, "Can't tranfer a -ve/zero sum"

        self.balance -= amount
        receiver.balance += amount

    def check_passwd(self, password):
        if self.__passwd == password:
            return True
        return False


class SavingsAccount(Account):
    def withdraw(self, amount):
        assert amount <= 200000, "SavingsAccount limit reached"
        assert amount > 0, "Can't withdraw a zero/-ve sum"

        self.balance -= amount

    def deposit(self, amount):
        assert amount <= 1000000, "SavingsAccount limit reached"
        assert amount > 0, "Can't deposit a zero/-ve sum"

        self.balance += amount

    def apply_interest(self):
        if (time() - self.created_on) >= 31536000:
            self.balance = self.balance + (self.balance * 0.07)


class CurrentAccount(Account):
    def withdraw(self, amount):
        assert amount > 0, "Can't withdraw a zero/-ve sum"

        self.balance -= amount

    def deposit(self, amount):
        assert amount > 0, "Can't deposit a zero/-ve sum"

        self.balance += amount

    def apply_interest(self):
        if (time() - self.created_on) >= 31536000:
            self.balance = self.balance + (self.balance * 0.05)
