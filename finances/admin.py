from django.contrib import admin
from .models import *


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('type', 'date', 'amount', 'category', 'notes')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'parent')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Transaction, TransactionAdmin)

