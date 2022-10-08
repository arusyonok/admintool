from django.db import models
from django.contrib import admin
from catalog.common import RecordTypes


class Category(models.Model):
    name = models.CharField(max_length=50)
    type = models.IntegerField(choices=RecordTypes.CHOICES, default=0)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
