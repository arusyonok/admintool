class RecordTypes:
    EXPENSE = 0
    INCOME = 1
    TRANSFER = 2

    CHOICES = (
        (EXPENSE, 'Expense'),
        (INCOME, 'Income'),
        (TRANSFER, 'Transfer'),
    )

    DICT = {
        "Expense": EXPENSE,
        "Income": INCOME,
        "Transfer": TRANSFER,
    }