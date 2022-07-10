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
    """
    An abstract class which partially imitates bank accounts

    Args:
        ABC : Abstract parent class
    """

    bank_name = "Void"

    def __init__(self, name, passwd, balance):
        assert balance > 0, "Can't create a account with zero/-ve funds"
        assert len(passwd) >= 8, "Please type a password of 8 or more characters"

        self.__balance = balance
        self.__name = name
        self.__passwd = passwd
        self.created_on = time()

    def __repr__(self) -> str:
        return f"Account({self.name})"

    @property
    def name(self) -> str:
        """Returns the value of private attribute 'name'

        Returns:
            str: "name"
        """
        return self.__name

    @property
    def balance(self) -> float:
        """Returns the value of private attribute 'balance'

        Returns:
            float: "balance"
        """
        return self.__balance

    @property
    def passwd(self) -> None:
        """Makes the private attribute 'passwd' inaccessible by returning 'None'

        Returns:
            None
        """
        return None

    @name.setter
    def name(self, new_name: str) -> None:
        assert new_name != self.__name, "Name already in use"

        self.__name = new_name

    @passwd.setter
    def passwd(self, new_passwd: str) -> None:
        assert new_passwd != self.__passwd, "Password already in use"
        assert len(new_passwd) >= 8, "Please type a password of 8 or more characters"

        self.__passwd = new_passwd

    @balance.setter
    def balance(self) -> None:
        pass

    @staticmethod
    def save(acc_obj) -> None:
        """
        A Function to save the account object to a '.pkl' file for
        data persistency
        It is a staticmethod so it can accesed without instantiating

        Args:
            acc_obj (module defined): The Account Object
        """
        with open(f"{acc_obj.name}.pkl", "wb") as file:
            dump(acc_obj, file, -1)

    @staticmethod
    def load(acc_name: str, password: str):
        """
        A Function which the account object from a '.pkl' file
        and to check if the request is from the owner of
        this object by validating it's password
        It is a staticmethod so it can accesed without instantiating

        Args:
            acc_name (str): Account's name
            password (str): User password

        Raises:
            Exception: If the given password is wrong it raises an exception

        Returns:
            Account: The object defined in this module
                or None if pickle file is not found
        """
        try:
            with open(f"{acc_name}.pkl", "rb") as file:
                tmp = load(file)
            if tmp.check_passwd(password):
                return tmp
            raise Exception("Wrong Password!")
        except FileNotFoundError:
            return None

    @abstractmethod
    def withdraw(self, amount: float) -> None:
        """
        A method to withdraw a sum from the account
        It is an abstractclass to apply limits on the 'amount' in the
        children classes

        Args:
            amount (float): The sum which is to be withdrawn
        """
        assert amount > 0, "Can't withdraw a zero/-ve sum"

        self.__balance -= amount

    @abstractmethod
    def deposit(self, amount: float) -> None:
        """
        A method to deposit a sum from the account
        It is an abstractclass to apply limits on the 'amount' in the
        children classes
        Args:
            amount (float): The sum which is to be deposited
        """
        assert amount > 0, "Can't deposit a zero/-ve sum"

        self.__balance += amount

    def transfer(self, amount: float, receiver) -> None:
        """
        A method to transfer money internally without any limits

        Args:
            amount (float): The sum to be transfered
            receiver : Receiver's account object
        """
        assert amount > 0, "Can't tranfer a -ve/zero sum"

        self.__balance -= amount
        receiver.receive_sum(amount)

    def receive_sum(self, amount: float) -> None:
        """
        A method to receive money internally without any limits

        Args:
            amount (float): The sum to be received
        """
        self.__balance += amount

    def check_passwd(self, password: str) -> bool:
        """
        A method to compare the private attribute 'passwd' to given
        arugement 'password'

        Args:
            password (str): The string which needs to be compared

        Returns:
            Boolean Value
        """
        if self.__passwd == password:
            return True
        return False

    def break_fd(self, fixed_deposit):
        """
        A method to break FD and add it to the instantiated object with
        interest

        Args:
            fixed_deposit : An object defined in this module
        """
        amount = fixed_deposit.balance + (fixed_deposit.balance * 0.09)
        self.__balance += amount
        remove(f"{fixed_deposit.name}.pkl")


class SavingsAccount(Account):
    """
    A children class of Account to encapsulate the amount which
    can be deposited/withdrawn

    Args:
        Account : Parent class
    """

    type = "Savings"

    def withdraw(self, amount):
        assert amount <= 200000, "SavingsAccount limit reached"
        assert amount > 0, "Can't withdraw a zero/-ve sum"

        self.__balance -= amount
        if self.__balance:
            pass

    def deposit(self, amount):
        assert amount <= 1000000, "SavingsAccount limit reached"
        assert amount > 0, "Can't deposit a zero/-ve sum"

        self.__balance += amount


class CurrentAccount(Account):
    """
    A children class of Account which has limits set on transaction
    according to the rules which are currently followed

    Args:
        Account : Parent class
    """

    type = "Current"

    def withdraw(self, amount):
        assert amount > 0, "Can't withdraw a zero/-ve sum"

        self.__balance -= amount
        if self.__balance:
            pass

    def deposit(self, amount):
        assert amount > 0, "Can't deposit a zero/-ve sum"

        self.__balance += amount


class FixedDeposit:
    """
    An object to imitate the Fixed Deposit present in the
    banking system
    """

    def __init__(self, name, passwd, balance, time_period):
        assert balance > 0, "Can't create a FD with zero/-ve sum"
        assert len(passwd) >= 8, "Please type a password of 8 or more characters"

        self.__balance = balance
        self.__passwd = passwd
        self.__name = name
        self.created_on = time()
        self.time_period = time_period

    @property
    def name(self) -> str:
        """
        Returns the value of private attribute 'name'

        Returns:
            str
        """
        return self.__name

    @property
    def balance(self) -> float:
        """
        Returns the value of private attribute 'balance'

        Returns:
            float
        """
        return self.__balance

    @property
    def passwd(self) -> None:
        """
        Makes the private attribute 'passwd' inaccessible by returning 'None'

        Returns:
            None/Null
        """
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

    def check_maturity(self) -> bool:
        """
        A method to check if the Time period of the FD has crossed its
        maturation date
        Returns:
            Boolean Value
        """
        curr_time = time()
        if curr_time - self.created_on >= self.time_period:
            return True
        return False
