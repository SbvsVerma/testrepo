"""
XYZ
"""

from abc import ABC, abstractmethod
from pickle import dump, load
from time import time
from os import remove


class Account(ABC):
    bank_name = "Void"

    def __init__(self, name, passwd, balance):
        assert balance > 0, "Can't create a account with zero/-ve funds"
        assert len(passwd) >= 8, "Please type a password of 8 or more characters"

        self.__balance = balance
        self.__name = name
        self.__passwd = passwd
        self.created_on = time()

    @property
    def name(self):
        return self.__name

    @property
    def balance(self):
        return self.__balance

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

    @balance.setter
    def balance(self):
        pass

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

        self.__balance -= amount

    @abstractmethod
    def deposit(self, amount):
        assert amount > 0, "Can't deposit a zero/-ve sum"

        self.__balance += amount

    @abstractmethod
    def apply_interest(self):
        if (time() - self.created_on) >= 31536000:
            self.__balance = self.__balance + (self.__balance * 0)

    def transfer(self, amount, receiver):
        assert amount > 0, "Can't tranfer a -ve/zero sum"

        self.__balance -= amount
        receiver.receive_sum(amount)

    def receive_sum(self, amount):
        self.__balance += amount

    def check_passwd(self, password):
        if self.__passwd == password:
            return True
        return False

    def break_fd(self, FD):
        amount = FD.balance + (FD.balance * 0.09)
        self.__balance += amount
        remove(f"{FD.name}.pkl")


class SavingsAccount(Account):
    type = "Savings"

    def withdraw(self, amount):
        assert amount <= 200000, "SavingsAccount limit reached"
        assert amount > 0, "Can't withdraw a zero/-ve sum"

        self.__balance -= amount

    def deposit(self, amount):
        assert amount <= 1000000, "SavingsAccount limit reached"
        assert amount > 0, "Can't deposit a zero/-ve sum"

        self.__balance += amount

    def apply_interest(self):
        if (time() - self.created_on) >= 31536000:
            self.__balance = self.__balance + (self.__balance * 0.07)


class CurrentAccount(Account):
    type = "Current"

    def withdraw(self, amount):
        assert amount > 0, "Can't withdraw a zero/-ve sum"

        self.__balance -= amount

    def deposit(self, amount):
        assert amount > 0, "Can't deposit a zero/-ve sum"

        self.__balance += amount

    def apply_interest(self):
        if (time() - self.created_on) >= 31536000:
            self.__balance = self.__balance + (self.__balance * 0.05)


class FixedDeposit:
    def __init__(self, name, passwd, balance, time_period):
        assert balance > 0, "Can't create a FD with zero/-ve sum"
        assert len(passwd) >= 8, "Please type a password of 8 or more characters"

        self.__balance = balance
        self.__passwd = passwd
        self.__name = name
        self.created_on = time()
        self.time_period = time_period

    @property
    def name(self):
        return self.__name

    @property
    def balance(self):
        return self.__balance

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

    @balance.setter
    def balance(self):
        pass

    def check_maturity(self):
        curr_time = time()
        if curr_time - self.created_on >= self.time_period:
            return True
        return False
