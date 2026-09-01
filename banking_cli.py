"""
banking_cli.py

Command-line interface for the banking system. Handles all user input/output;
the actual account rules live in accounts.py and know nothing about the CLI.
"""

from decimal import Decimal, InvalidOperation

from accounts import SavingsAccount, CurrentAccount

MENU = (
    "\nBanking System Menu:\n"
    "1. Create a new account\n"
    "2. Deposit money\n"
    "3. Withdraw money\n"
    "4. Display account details\n"
    "5. Calculate interest (Savings Account)\n"
    "6. Exit"
)


def prompt_amount(label: str) -> Decimal:
    """Keep asking until the user enters a valid amount, instead of crashing on bad input."""
    while True:
        raw = input(label)
        try:
            return Decimal(raw)
        except InvalidOperation:
            print("Please enter a valid number (e.g. 100 or 49.99).")


def run() -> None:
    accounts = {}

    while True:
        print(MENU)
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            account_number = input("Enter account number: ").strip()
            if account_number in accounts:
                print("An account with that number already exists.")
                continue

            account_holder = input("Enter account holder name: ").strip()
            account_type = input("Enter account type (Savings/Current): ").strip().lower()

            if account_type == "savings":
                accounts[account_number] = SavingsAccount(account_number, account_holder)
                print("Savings account created successfully.")
            elif account_type == "current":
                accounts[account_number] = CurrentAccount(account_number, account_holder)
                print("Current account created successfully.")
            else:
                print("Invalid account type.")

        elif choice == "2":
            account_number = input("Enter account number: ").strip()
            if account_number not in accounts:
                print("Account not found.")
                continue
            amount = prompt_amount("Enter deposit amount: ")
            _, message = accounts[account_number].deposit(amount)
            print(message)

        elif choice == "3":
            account_number = input("Enter account number: ").strip()
            if account_number not in accounts:
                print("Account not found.")
                continue
            amount = prompt_amount("Enter withdrawal amount: ")
            _, message = accounts[account_number].withdraw(amount)
            print(message)

        elif choice == "4":
            account_number = input("Enter account number: ").strip()
            if account_number in accounts:
                print(accounts[account_number].show_details())
            else:
                print("Account not found.")

        elif choice == "5":
            account_number = input("Enter account number: ").strip()
            account = accounts.get(account_number)
            if isinstance(account, SavingsAccount):
                print(f"Interest earned: {account.calculate_interest()}")
            else:
                print("Account not found or not a Savings Account.")

        elif choice == "6":
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    run()
