from django.db import models
from django.contrib import admin
from catalog.common import RecordTypes


class Category(models.Model):
    name = models.CharField(max_length=50)
    type = models.IntegerField(choices=RecordTypes.CHOICES, default=0)

    class Meta:
        verbose_name = "Categories"

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Sub Categories"

    def __str__(self):
        return self.name
