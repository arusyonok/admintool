from django.contrib import admin
from .models import *


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('type', 'date', 'amount', 'notes')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')

admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Transaction, TransactionAdmin)

