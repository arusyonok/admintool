from django.db import models
from django.contrib import admin
from authorization.models import User, SpendingGroup
from catalog.common import RecordTypes
from catalog.models import SubCategory


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
    type = models.IntegerField(choices=RecordTypes.CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class SpendingGroupRecord(AbstractRecord):
    group = models.ForeignKey(SpendingGroup, on_delete=models.CASCADE)
    paid_by = models.ForeignKey(User, related_name="paid_by_me_set", on_delete=models.SET_NULL, null=True)
    paid_for_users = models.ManyToManyField(User, related_name="paid_for_me_set")

    def is_group(self):
        return False if self.group_id is None else True
