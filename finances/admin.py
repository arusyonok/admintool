from django.contrib import admin
from .models import *


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('type', 'date', 'amount', 'category', 'account', 'get_account_type', 'notes')

    def get_account_type(self, obj):
        return obj.account.type

    get_account_type.short_description = 'Account Type'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'parent')

admin.site.register(Category, CategoryAdmin)
admin.site.register(AccountType)
admin.site.register(Account)
admin.site.register(Transaction, TransactionAdmin)

