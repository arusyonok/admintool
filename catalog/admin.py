from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')


class SubCategoryKeywordsAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'sub_category')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(SubCategoryKeywords, SubCategoryKeywordsAdmin)
admin.site.register(Tag, TagAdmin)
