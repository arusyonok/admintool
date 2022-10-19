from django import forms
from accounts.models import Profile
from catalog.models import SubCategory
from catalog.common import RecordTypes
from .models import PersonalWalletRecord, GroupWalletRecord


class PersonalRecordCreateForm(forms.ModelForm):
    record_type = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = PersonalWalletRecord
        fields = ["title", "amount", "record_type", "sub_category"]


class ExpenseCreateForm(PersonalRecordCreateForm):
    sub_category = forms.ModelChoiceField(queryset=SubCategory.objects.filter(parent__type=RecordTypes.EXPENSE),
                                          required=False)

    def clean_record_type(self):
        return RecordTypes.EXPENSE


class IncomeCreateForm(PersonalRecordCreateForm):
    sub_category = forms.ModelChoiceField(queryset=SubCategory.objects.filter(parent__type=RecordTypes.INCOME),
                                          required=False)

    def clean_record_type(self):
        return RecordTypes.INCOME


class PersonalRecordUpdateForm(forms.ModelForm):
    record_type = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = PersonalWalletRecord
        fields = ["title", "amount", "record_type", "sub_category"]


class ExpenseUpdateForm(PersonalRecordUpdateForm):
    sub_category = forms.ModelChoiceField(queryset=SubCategory.objects.filter(parent__type=RecordTypes.EXPENSE),
                                          required=False)

    def clean_record_type(self):
        return RecordTypes.EXPENSE


class IncomeUpdateForm(PersonalRecordUpdateForm):
    sub_category = forms.ModelChoiceField(queryset=SubCategory.objects.filter(parent__type=RecordTypes.INCOME),
                                          required=False)

    def clean_record_type(self):
        return RecordTypes.INCOME


class GroupExpenseCreateForm(forms.ModelForm):
    record_type = forms.CharField(widget=forms.HiddenInput(), required=False)
    sub_category = forms.ModelChoiceField(queryset=SubCategory.objects.filter(parent__type=RecordTypes.EXPENSE),
                                          required=False)
    paid_by = forms.ModelChoiceField(queryset=Profile.objects.all())
    paid_for_users = forms.MultipleChoiceField()

    class Meta:
        model = GroupWalletRecord
        fields = ["title", "amount", "paid_by", "paid_for_users", "record_type", "sub_category"]

    def __init__(self, wallet_pk=None, *args, **kwargs):
        super(GroupExpenseCreateForm, self).__init__(*args, **kwargs)
        choices_list = []
        wallet_users = Profile.objects.filter(wallet__id=wallet_pk)
        for user in wallet_users:
            choices_list.append((user.id, user))
        self.fields["paid_for_users"].choices = choices_list
        self.fields["paid_by"].queryset = wallet_users

    def clean_record_type(self):
        return RecordTypes.EXPENSE


class GroupExpenseUpdateForm(forms.ModelForm):
    record_type = forms.CharField(widget=forms.HiddenInput(), required=False)
    sub_category = forms.ModelChoiceField(queryset=SubCategory.objects.filter(parent__type=RecordTypes.EXPENSE),
                                          required=False)
    paid_by = forms.ModelChoiceField(queryset=Profile.objects.all())
    paid_for_users = forms.MultipleChoiceField()

    class Meta:
        model = GroupWalletRecord
        fields = ["title", "amount", "paid_by", "paid_for_users", "record_type", "sub_category"]

    def __init__(self, wallet_pk=None, *args, **kwargs):
        super(GroupExpenseUpdateForm, self).__init__(*args, **kwargs)
        choices_list = []
        wallet_users = Profile.objects.filter(wallet__id=wallet_pk)
        for user in wallet_users:
            choices_list.append((user.id, user))
        self.fields["paid_for_users"].choices = choices_list
        self.fields["paid_by"].queryset = wallet_users

    def clean_record_type(self):
        return RecordTypes.EXPENSE
