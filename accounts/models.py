from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):

    class Meta:
        verbose_name = "Profile"

    def __str__(self):
        if self.first_name or self.last_name:
            full_name = f"{self.first_name} {self.last_name} ({self.username})"
            no_first_name = f"{self.last_name} ({self.username})"
            display_name = full_name if self.first_name else no_first_name
        else:
            display_name = self.username

        return display_name

    def personal_wallets(self):
        return [acc for acc in self.wallet_set.all() if acc.is_personal_wallet]

    def group_wallets(self):
        return [acc for acc in self.wallet_set.all() if acc.is_group_wallet]


class Wallet(models.Model):
    title = models.CharField(max_length=50)
    users = models.ManyToManyField(Profile)

    def __str__(self):
        return self.title

    @property
    def is_group_wallet(self):
        return True if self.users.count() >= 2 else False

    @property
    def is_personal_wallet(self):
        return True if self.users.count() == 1 else False

