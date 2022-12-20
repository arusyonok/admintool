from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Tag, TagAdmin)
