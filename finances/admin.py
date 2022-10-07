from django import forms
from django.core.exceptions import ValidationError
from django.contrib import admin
from .models import *


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



class PersonalRecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'date', 'sub_category', 'type', 'user')


class SpendingGroupRecordForm(forms.ModelForm):
    class Meta:
        model = SpendingGroupRecord
        fields = ['title', 'amount', 'sub_category', 'group', 'paid_by', 'paid_for_users']

    def clean_paid_by(self):
        paid_by = self.cleaned_data['paid_by']
        all_users_in_group = self.cleaned_data["group"].users.all().values_list("id", flat=True)

        if paid_by.id not in all_users_in_group:
             raise ValidationError('Payer is not in this group!')

        return paid_by


    def clean_paid_for_users(self):
        paid_for_users = self.cleaned_data['paid_for_users']
        all_users_in_group = list(self.cleaned_data["group"].users.all().values_list("id", flat=True))

        paid_for_users_ids = list(paid_for_users.values_list("id", flat=True))
        if paid_for_users_ids != all_users_in_group:
             raise ValidationError('Payee is not in this group!')

        return paid_for_users


class SpendingGroupRecordAdmin(admin.ModelAdmin):
    form = SpendingGroupRecordForm
    list_display = ('group', 'title', 'amount', 'date', 'category', 'sub_category', 'paid_by',
                    'paid_for_users_string')

    def paid_for_users_string(self, obj):
        return ", ".join([f"{user}" for user in obj.paid_for_users.all()])


    def category(self, obj):
        return obj.sub_category.parent


admin.site.register(SpendingGroupRecord, SpendingGroupRecordAdmin)
admin.site.register(PersonalRecord, PersonalRecordAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(SpendingGroup, SpendingGroupAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
