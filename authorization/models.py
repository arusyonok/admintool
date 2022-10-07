from django.db import models
from django.contrib import admin


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
