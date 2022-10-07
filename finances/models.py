from django.db import models
from django.contrib import admin


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


class AbstractRecord(models.Model):
    title = models.CharField(max_length=50)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateTimeField(auto_now_add=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PersonalRecord(AbstractRecord):
    type = models.IntegerField(choices=RECORD_TYPES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class SpendingGroupRecord(AbstractRecord):
    group = models.ForeignKey(SpendingGroup, on_delete=models.CASCADE)
    paid_by = models.ForeignKey(User, related_name="paid_by_me_set", on_delete=models.SET_NULL, null=True)
    paid_for_users = models.ManyToManyField(User, related_name="paid_for_me_set")

    def is_group(self):
        return False if self.group_id is None else True