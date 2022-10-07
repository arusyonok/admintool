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


class User(models.Model):
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        if self.first_name or self.last_name:
            full_name = f"{self.first_name} {self.last_name} ({self.username})"
            no_first_name = f"{self.last_name} ({self.username})"
            display_name = full_name if self.first_name else no_first_name
        else:
            display_name = self.username

        return display_name


class SpendingGroup(models.Model):
    title = models.CharField(max_length=50)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.title


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
