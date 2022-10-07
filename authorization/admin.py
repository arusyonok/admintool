from django import forms
from django.core.exceptions import ValidationError
from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name')


class SpendingGroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'group_members')

    def group_members(self, obj):
        return ", ".join([f"{user}" for user in obj.users.all()])


admin.site.register(User, UserAdmin)
admin.site.register(SpendingGroup, SpendingGroupAdmin)
