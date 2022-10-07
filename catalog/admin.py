from django import forms
from django.core.exceptions import ValidationError
from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')

admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
