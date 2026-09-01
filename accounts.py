"""
accounts.py

Core account classes for the banking system.

Design note: business logic methods return a (success: bool, message: str)
tuple instead of printing directly. This keeps the classes testable and
decoupled from however the results get displayed (CLI, GUI, API, etc.).
"""

from datetime import date
from decimal import Decimal, InvalidOperation


class Account:
    """Base account with deposit/withdraw behaviour shared by all account types."""

    def __init__(self, account_number: str, account_holder: str, balance="0"):
        self.account_number = account_number
        self.account_holder = account_holder
        self._balance = self._to_decimal(balance)

    @staticmethod
    def _to_decimal(value) -> Decimal:
        """Convert user input into a Decimal, raising a clear error if it's invalid."""
        try:
            return Decimal(str(value))
        except InvalidOperation:
            raise ValueError(f"'{value}' is not a valid monetary amount.")

    @property
    def balance(self) -> Decimal:
        """Read-only balance — change it only through deposit()/withdraw()."""
        return self._balance

    def deposit(self, amount) -> tuple[bool, str]:
        """Add funds to the account. Returns (success, message)."""
        amount = self._to_decimal(amount)
        if amount <= 0:
            return False, "Deposit amount must be positive."
        self._balance += amount
        return True, f"Deposited {amount}. New balance: {self._balance}"

    def withdraw(self, amount) -> tuple[bool, str]:
        """Remove funds from the account. Returns (success, message)."""
        amount = self._to_decimal(amount)
        if amount <= 0:
            return False, "Withdrawal amount must be positive."
        if amount > self._balance:
            return False, "Insufficient funds."
        self._balance -= amount
        return True, f"Withdrew {amount}. New balance: {self._balance}"

    def show_details(self) -> str:
        return (
            f"Account Number: {self.account_number}\n"
            f"Account Holder: {self.account_holder}\n"
            f"Balance: {self._balance}"
        )


class SavingsAccount(Account):
    """Savings account: earns interest, capped at a limited number of withdrawals per month."""

    MONTHLY_WITHDRAWAL_LIMIT = 3

    def __init__(self, account_number: str, account_holder: str, balance="0", interest_rate="5"):
        super().__init__(account_number, account_holder, balance)
        self.interest_rate = self._to_decimal(interest_rate)
        self._withdrawals_this_month = 0
        self._current_period = date.today().replace(day=1)

    def _reset_if_new_month(self) -> None:
        """The withdrawal count resets automatically once a new calendar month starts."""
        this_month = date.today().replace(day=1)
        if this_month != self._current_period:
            self._current_period = this_month
            self._withdrawals_this_month = 0

    def calculate_interest(self) -> Decimal:
        return self._balance * (self.interest_rate / Decimal("100"))

    def withdraw(self, amount) -> tuple[bool, str]:
        self._reset_if_new_month()
        if self._withdrawals_this_month >= self.MONTHLY_WITHDRAWAL_LIMIT:
            return False, f"Withdrawal limit reached ({self.MONTHLY_WITHDRAWAL_LIMIT} per month)."

        success, message = super().withdraw(amount)
        if success:
            self._withdrawals_this_month += 1
        return success, message


class CurrentAccount(Account):
    """Current account: allows withdrawals into a fixed overdraft limit."""

    def __init__(self, account_number: str, account_holder: str, balance="0", overdraft_limit="1000"):
        super().__init__(account_number, account_holder, balance)
        self.overdraft_limit = self._to_decimal(overdraft_limit)

    def withdraw(self, amount) -> tuple[bool, str]:
        amount = self._to_decimal(amount)
        if amount <= 0:
            return False, "Withdrawal amount must be positive."
        if self._balance - amount < -self.overdraft_limit:
            return False, "Withdrawal exceeds overdraft limit."
        self._balance -= amount
        return True, f"Withdrew {amount}. New balance: {self._balance}"
