from django import forms
from django.core.exceptions import ValidationError
from django.contrib import admin
from .models import *


class PersonalWalletRecordForm(forms.ModelForm):
    class Meta:
        model = PersonalWalletRecord
        fields = ['title', 'amount', 'sub_category', 'record_type', 'user', 'personal_wallet']

    def clean_personal_wallet(self):
        personal_wallet = self.cleaned_data['personal_wallet']
        user = self.cleaned_data['user']
        users_in_wallet = self.cleaned_data["personal_wallet"].users.all().values_list("id", flat=True)

        if user.id not in users_in_wallet:
             raise ValidationError('User does not have this wallet')

        if not personal_wallet.is_personal_wallet:
             raise ValidationError('This is not a personal wallet')

        return personal_wallet


class PersonalWalletRecordAdmin(admin.ModelAdmin):
    form = PersonalWalletRecordForm
    list_display = ('title', 'amount', 'date', 'sub_category', 'record_type', 'user')


class GroupWalletRecordForm(forms.ModelForm):
    class Meta:
        model = GroupWalletRecord
        fields = ['title', 'amount', 'sub_category', 'group_wallet', 'paid_by', 'paid_for_users']

    def clean_paid_by(self):
        paid_by = self.cleaned_data['paid_by']
        all_users_in_group = self.cleaned_data["group_wallet"].users.all().values_list("id", flat=True)

        if paid_by.id not in all_users_in_group:
             raise ValidationError('Payer is not in this group!')

        return paid_by

    def clean_paid_for_users(self):
        paid_for_users = self.cleaned_data['paid_for_users']
        all_users_in_group = list(self.cleaned_data["group_wallet"].users.all().values_list("id", flat=True))

        paid_for_users_ids = list(paid_for_users.values_list("id", flat=True))
        if not any(user_id in all_users_in_group for user_id in paid_for_users_ids):
             raise ValidationError('Payee is not in this group!')

        return paid_for_users


class GroupWalletRecordAdmin(admin.ModelAdmin):
    form = GroupWalletRecordForm
    list_display = ('group_wallet', 'title', 'amount', 'date', 'category', 'sub_category', 'paid_by',
                    'paid_for_users_string')

    def paid_for_users_string(self, obj):
        return ", ".join([f"{user}" for user in obj.paid_for_users.all()])

    def category(self, obj):
        return obj.sub_category.parent


admin.site.register(GroupWalletRecord, GroupWalletRecordAdmin)
admin.site.register(PersonalWalletRecord, PersonalWalletRecordAdmin)
