from django.db import models
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


class SubCategoryKeywords(models.Model):
    keyword = models.CharField(max_length=100)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
