from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name')


class WalletAdmin(admin.ModelAdmin):
    list_display = ('title', 'group_members')

    def group_members(self, obj):
        return ", ".join([f"{user}" for user in obj.users.all()])


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Wallet, WalletAdmin)
