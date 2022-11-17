from django.db import models
from accounts.models import Profile, Wallet
from catalog.common import RecordTypes
from catalog.models import SubCategory
from decimal import Decimal


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


class PersonalWalletRecord(AbstractRecord):
    personal_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    record_type = models.IntegerField(choices=RecordTypes.CHOICES)


class GroupWalletRecord(AbstractRecord):
    group_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    paid_by = models.ForeignKey(Profile, related_name="paid_by_me_set", on_delete=models.SET_NULL, null=True)
    paid_for_users = models.ManyToManyField(Profile, related_name="paid_for_me_set")


class Balance(models.Model):
    loaned_from = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="balance_set_loaned_by_me")
    loaned_to = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="balance_set_loaned_to_me")
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=Decimal(0))
    group_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
