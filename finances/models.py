from django.db import models
from accounts.models import Profile, GroupAccount
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

    @property
    def category(self):
        return self.sub_category.parent


class PersonalRecord(AbstractRecord):
    type = models.IntegerField(choices=RecordTypes.CHOICES)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)


class GroupAccountRecord(AbstractRecord):
    group_account = models.ForeignKey(GroupAccount, on_delete=models.CASCADE)
    paid_by = models.ForeignKey(Profile, related_name="paid_by_me_set", on_delete=models.SET_NULL, null=True)
    paid_for_users = models.ManyToManyField(Profile, related_name="paid_for_me_set")

    def is_group_account(self):
        return False if self.group_account is None else True
