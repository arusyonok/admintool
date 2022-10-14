from django import forms
from django.core.exceptions import ValidationError
from django.contrib import admin
from .models import *


class PersonalRecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'date', 'sub_category', 'type', 'user')


class GroupAccountRecordForm(forms.ModelForm):
    class Meta:
        model = GroupAccountRecord
        fields = ['title', 'amount', 'sub_category', 'group_account', 'paid_by', 'paid_for_users']

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


class GroupAccountRecordAdmin(admin.ModelAdmin):
    form = GroupAccountRecordForm
    list_display = ('group_account', 'title', 'amount', 'date', 'category', 'sub_category', 'paid_by',
                    'paid_for_users_string')

    def paid_for_users_string(self, obj):
        return ", ".join([f"{user}" for user in obj.paid_for_users.all()])


    def category(self, obj):
        return obj.sub_category.parent


admin.site.register(GroupAccountRecord, GroupAccountRecordAdmin)
admin.site.register(PersonalRecord, PersonalRecordAdmin)
