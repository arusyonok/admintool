from django.db import models
from django.contrib import admin


TRANSACTION_TYPES = (
    (0, 'Expense'),
    (1, 'Income'),
    (2, 'Transfer'),
)

TRANSACTION_TYPE_ID = (
    ('expense', 0),
    ('income', 1),
    ('transfer', 2),
)

RECORD_TYPES = (
    (0, 'Expense'),
    (1, 'Income'),
    (2, "Transfer")
)

class Category(models.Model):
    name = models.CharField(max_length=50)
    type = models.IntegerField(choices=RECORD_TYPES, default=0) # TODO: fix this default

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    type = models.IntegerField(choices=TRANSACTION_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    notes = models.TextField()
