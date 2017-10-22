from django.db import models

TRANSACTION_TYPES = (
    (0, 'E'),
    (1, 'I'),
    (2, 'T'),
)


class ParentCategory(models.Model):
    name = models.CharField(max_length=50)


class Category(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey(ParentCategory, on_delete=models.CASCADE)


class AccountType(models.Model):
    name = models.CharField(max_length=50)


class Account(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(AccountType)


class Transaction(models.Model):
    type = models.IntegerField(choices=TRANSACTION_TYPES)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    amount = models.FloatField()
    category = models.ForeignKey(Category)
    account = models.ForeignKey(Account)
    notes = models.TextField()
