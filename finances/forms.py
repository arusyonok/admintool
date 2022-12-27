import datetime
from django import forms
from accounts.models import Profile
from catalog.models import SubCategory, Tag
from catalog.common import RecordTypes
from .models import PersonalWalletRecord, GroupWalletRecord


class PersonalRecordCreateForm(forms.ModelForm):
    date = forms.DateField(input_formats=['%d/%m/%Y'])
    record_type = forms.CharField(widget=forms.HiddenInput(), required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)

    class Meta:
        model = PersonalWalletRecord
        fields = ["title", "amount", "date", "record_type", "sub_category", "tags"]

    def clean_date(self):
        date = self.cleaned_data['date']
        if date > datetime.date.today():
            raise forms.ValidationError("The date cannot be in the future!")
        return date


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
    date = forms.DateField(input_formats=['%d/%m/%Y'])
    record_type = forms.CharField(widget=forms.HiddenInput(), required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)

    class Meta:
        model = PersonalWalletRecord
        fields = ["title", "amount", "date", "record_type", "sub_category", "tags"]

    def clean_date(self):
        date = self.cleaned_data['date']
        if date > datetime.date.today():
            raise forms.ValidationError("The date cannot be in the future!")
        return date


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
    date = forms.DateField(input_formats=['%d/%m/%Y'])
    record_type = forms.CharField(widget=forms.HiddenInput(), required=False)
    sub_category = forms.ModelChoiceField(queryset=SubCategory.objects.filter(parent__type=RecordTypes.EXPENSE),
                                          required=False)
    paid_by = forms.ModelChoiceField(queryset=Profile.objects.all())
    paid_for_users = forms.MultipleChoiceField()

    class Meta:
        model = GroupWalletRecord
        fields = ["title", "amount", "date", "paid_by", "paid_for_users", "record_type", "sub_category"]

    def __init__(self, wallet_id=None, *args, **kwargs):
        super(GroupExpenseCreateForm, self).__init__(*args, **kwargs)
        choices_list = []
        wallet_users = Profile.objects.filter(wallet__id=wallet_id)
        for user in wallet_users:
            choices_list.append((user.id, user))
        self.fields["paid_for_users"].choices = choices_list
        self.fields["paid_by"].queryset = wallet_users

    def clean_record_type(self):
        return RecordTypes.EXPENSE

    def clean_date(self):
        date = self.cleaned_data['date']
        if date > datetime.date.today():
            raise forms.ValidationError("The date cannot be in the future!")
        return date


class GroupExpenseUpdateForm(forms.ModelForm):
    date = forms.DateField(input_formats=['%d/%m/%Y'])
    record_type = forms.CharField(widget=forms.HiddenInput(), required=False)
    sub_category = forms.ModelChoiceField(queryset=SubCategory.objects.filter(parent__type=RecordTypes.EXPENSE),
                                          required=False)
    paid_by = forms.ModelChoiceField(queryset=Profile.objects.all())
    paid_for_users = forms.MultipleChoiceField()

    class Meta:
        model = GroupWalletRecord
        fields = ["title", "amount", "date", "paid_by", "paid_for_users", "record_type", "sub_category"]

    def __init__(self, wallet_id=None, *args, **kwargs):
        super(GroupExpenseUpdateForm, self).__init__(*args, **kwargs)
        choices_list = []
        wallet_users = Profile.objects.filter(wallet__id=wallet_id)
        for user in wallet_users:
            choices_list.append((user.id, user))
        self.fields["paid_for_users"].choices = choices_list
        self.fields["paid_by"].queryset = wallet_users

    def clean_record_type(self):
        return RecordTypes.EXPENSE

    def clean_date(self):
        date = self.cleaned_data['date']
        if date > datetime.date.today():
            raise forms.ValidationError("The date cannot be in the future!")
        return date


class BulkUpdateRecordsForm(forms.Form):
    sub_category = forms.ModelChoiceField(queryset=SubCategory.objects.all())


class BulkUpdatePersonalRecordsForm(BulkUpdateRecordsForm):
    records = forms.ModelMultipleChoiceField(queryset=PersonalWalletRecord.objects.all(),
                                             widget=forms.MultipleHiddenInput)


class BulkUpdateGroupRecordsForm(BulkUpdateRecordsForm):
    records = forms.ModelMultipleChoiceField(queryset=GroupWalletRecord.objects.all(),
                                             widget=forms.MultipleHiddenInput)
