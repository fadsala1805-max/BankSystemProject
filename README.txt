Banking System Project

A command-line banking program I built to practice OOP in Python — inheritance, polymorphism. It started as a class exercise (a base Account class with SavingsAccount and CurrentAccount subclasses), then I went back and cleaned it up so it's testable.

How it's organized:
- accounts.py — the actual account logic (deposits, withdrawals, interest calculation)
- banking_cli.py — the menu you interact with when you run the program
- test_accounts.py — unit tests for the account logic

I split it this way on purpose. Originally everything lived in one file that just printed results directly, which meant there was no real way to test any of it. Now the account methods return a result instead of printing, so the logic can be tested completely on its own, without needing to simulate typing into a menu.

New Updates:
- Switched from float to Decimal for money, since floats can introduce small rounding errors 
- Made balance read olny so it can only change through deposit()/ withdraw(), not by just setting it directly
- The savings withdrawal limit actually resets every month now, instead of just counting up forever
- Typing something invalid (letters where an amount is expected) no longer crashes the whole program, retry is requested

Running it:
\`\`\`bash
python banking_cli.py
\`\`\`

Running the tests:
\`\`\`bash
python -m unittest discover -s tests -t .
\`\`\`