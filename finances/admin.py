from django import forms
from django.contrib import admin
from .models import *


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('type', 'date', 'amount', 'notes')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name')


class SpendingGroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'group_members')

    def group_members(self, obj):
        return ", ".join([f"{user}" for user in obj.users.all()])

admin.site.register(User, UserAdmin)
admin.site.register(SpendingGroup, SpendingGroupAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Transaction, TransactionAdmin)
