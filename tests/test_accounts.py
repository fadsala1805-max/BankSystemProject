"""
test_accounts.py

Unit tests for accounts.py. Run with: python -m pytest
(or: python -m unittest discover)

This is the whole point of the refactor — the original version printed
everything, so there was nothing here to actually assert against.
"""

import unittest
from decimal import Decimal

from accounts import Account, SavingsAccount, CurrentAccount


class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account("001", "John Doe", balance="100")

    def test_deposit_increases_balance(self):
        success, _ = self.account.deposit("50")
        self.assertTrue(success)
        self.assertEqual(self.account.balance, Decimal("150"))

    def test_deposit_rejects_negative_amount(self):
        success, message = self.account.deposit("-10")
        self.assertFalse(success)
        self.assertEqual(self.account.balance, Decimal("100"))
        self.assertIn("positive", message)

    def test_withdraw_decreases_balance(self):
        success, _ = self.account.withdraw("40")
        self.assertTrue(success)
        self.assertEqual(self.account.balance, Decimal("60"))

    def test_withdraw_rejects_insufficient_funds(self):
        success, message = self.account.withdraw("1000")
        self.assertFalse(success)
        self.assertEqual(self.account.balance, Decimal("100"))
        self.assertIn("Insufficient funds", message)

    def test_invalid_amount_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.account.deposit("not-a-number")


class TestSavingsAccount(unittest.TestCase):
    def setUp(self):
        self.account = SavingsAccount("002", "John Doe", balance="1000", interest_rate="5")

    def test_calculate_interest(self):
        self.assertEqual(self.account.calculate_interest(), Decimal("50.00"))

    def test_withdrawal_limit_enforced(self):
        for _ in range(SavingsAccount.MONTHLY_WITHDRAWAL_LIMIT):
            success, _ = self.account.withdraw("10")
            self.assertTrue(success)

        success, message = self.account.withdraw("10")
        self.assertFalse(success)
        self.assertIn("Withdrawal limit reached", message)


class TestCurrentAccount(unittest.TestCase):
    def setUp(self):
        self.account = CurrentAccount("003", "John Doe", balance="0", overdraft_limit="500")

    def test_withdraw_within_overdraft_succeeds(self):
        success, _ = self.account.withdraw("300")
        self.assertTrue(success)
        self.assertEqual(self.account.balance, Decimal("-300"))

    def test_withdraw_beyond_overdraft_fails(self):
        success, message = self.account.withdraw("600")
        self.assertFalse(success)
        self.assertEqual(self.account.balance, Decimal("0"))
        self.assertIn("exceeds overdraft limit", message)


if __name__ == "__main__":
    unittest.main()
