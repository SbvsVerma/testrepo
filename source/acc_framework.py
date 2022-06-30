"""
Object based Frameworks for bank accounts
    Acount -> Abstract Class
    Savings & Current -> Children classes of Account
    FixedDeposit -> Independent Class
"""

from abc import ABC, abstractmethod
from pickle import dump, load
from time import time
from os import remove


class Account(ABC):
    """An abstract class which partially imitates bank accounts"""

    bank_name = "Void"

    def __init__(self, name, passwd, balance):
        assert balance > 0, "Can't create a account with zero/-ve funds"
        assert len(passwd) >= 8, "Please type a password of 8 or more characters"

        self.__balance = balance
        self.__name = name
        self.__passwd = passwd
        self.created_on = time()

    def __repr__(self):
        return f"Account({self.name})"

    @property
    def name(self):
        """Returns the value of private attribute 'name'"""
        return self.__name

    @property
    def balance(self):
        """Returns the value of private attribute 'balance'"""
        return self.__balance

    @property
    def passwd(self):
        """Makes the private attribute 'passwd' inaccessible by returning 'None'"""
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
        """A Function to save the account object to a '.pkl' file for
        data persistency

        It is a staticmethod so it can accesed without instantiating"""
        with open(f"{acc_obj.name}.pkl", "wb") as file:
            dump(acc_obj, file, -1)

    @staticmethod
    def load(acc_name, password):
        """A Function which the account object from a '.pkl' file
        passwd -> To check if the request is from the owner of
        this object

        It is a staticmethod so it can accesed without instantiating"""
        try:
            with open(f"{acc_name}.pkl", "rb") as file:
                tmp = load(file)
            if tmp.check_passwd(password):
                return tmp
            raise Exception("Wrong Password!")
        except FileNotFoundError:
            return None

    @abstractmethod
    def withdraw(self, amount):
        """
        A method to withdraw a sum from the account
            amount -> The sum which is to be withdrawn

        It is an abstractclass to apply limits on the 'amount' in the
        children classes"""
        assert amount > 0, "Can't withdraw a zero/-ve sum"

        self.__balance -= amount

    @abstractmethod
    def deposit(self, amount):
        """
        A method to deposit a sum from the account
            amount -> The sum which is to be deposited

        It is an abstractclass to apply limits on the 'amount' in the
        children classes"""
        assert amount > 0, "Can't deposit a zero/-ve sum"

        self.__balance += amount

    def transfer(self, amount, receiver):
        """A method to transfer money internally without any limits
        amount -> The sum to be transfered
        receiver -> Receiver's account object"""
        assert amount > 0, "Can't tranfer a -ve/zero sum"

        self.__balance -= amount
        receiver.receive_sum(amount)

    def receive_sum(self, amount):
        """A method to receive money internally without any limits
        amount -> The sum to be received"""
        self.__balance += amount

    def check_passwd(self, password):
        """A method to compare the private attribute 'passwd' to given
        arugement 'password'."""
        if self.__passwd == password:
            return True
        return False

    def break_fd(self, fixed_deposit):
        """A method to break FD and add it to the instantiated object with
        interest"""
        amount = fixed_deposit.balance + (fixed_deposit.balance * 0.09)
        self.__balance += amount
        remove(f"{fixed_deposit.name}.pkl")


class SavingsAccount(Account):
    """A children class of Account to encapsulate the amount which
    can be deposited/withdrawn"""

    type = "Savings"

    def withdraw(self, amount):
        assert amount <= 200000, "SavingsAccount limit reached"
        assert amount > 0, "Can't withdraw a zero/-ve sum"

        self.__balance -= amount

    def deposit(self, amount):
        assert amount <= 1000000, "SavingsAccount limit reached"
        assert amount > 0, "Can't deposit a zero/-ve sum"

        self.__balance += amount


class CurrentAccount(Account):
    """A children class of Account which has limits set on transaction
    according to the rules which are currently followed"""

    type = "Current"

    def withdraw(self, amount):
        assert amount > 0, "Can't withdraw a zero/-ve sum"

        self.__balance -= amount

    def deposit(self, amount):
        assert amount > 0, "Can't deposit a zero/-ve sum"

        self.__balance += amount


class FixedDeposit:
    """An object to imitate the Fixed Deposit present in the
    banking system"""

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
        """Returns the value of private attribute 'name'"""
        return self.__name

    @property
    def balance(self):
        """Returns the value of private attribute 'balance'"""
        return self.__balance

    @property
    def passwd(self):
        """Makes the private attribute 'passwd' inaccessible by returning 'None'"""
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
        """A method to check if the Time period of the FD has crossed its
        maturation date"""
        curr_time = time()
        if curr_time - self.created_on >= self.time_period:
            return True
        return False
