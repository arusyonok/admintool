from django import forms
from catalog.models import SubCategory
from catalog.common import RecordTypes
from .models import PersonalRecord


class PersonalRecordCreateForm(forms.ModelForm):
    type = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = PersonalRecord
        fields = ["title", "amount", "type", "sub_category"]


class ExpenseCreateForm(PersonalRecordCreateForm):
    sub_category = forms.ModelChoiceField(queryset=SubCategory.objects.filter(parent__type=RecordTypes.EXPENSE),
                                          required=False)

    def clean_type(self):
        return RecordTypes.EXPENSE


class IncomeCreateForm(PersonalRecordCreateForm):
    sub_category = forms.ModelChoiceField(queryset=SubCategory.objects.filter(parent__type=RecordTypes.INCOME),
                                          required=False)

    def clean_type(self):
        return RecordTypes.INCOME


class PersonalRecordUpdateForm(forms.ModelForm):
    type = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = PersonalRecord
        fields = ["title", "amount", "type", "sub_category"]


class ExpenseUpdateForm(PersonalRecordUpdateForm):
    sub_category = forms.ModelChoiceField(queryset=SubCategory.objects.filter(parent__type=RecordTypes.EXPENSE),
                                          required=False)

    def clean_type(self):
        return RecordTypes.EXPENSE


class IncomeUpdateForm(PersonalRecordUpdateForm):
    sub_category = forms.ModelChoiceField(queryset=SubCategory.objects.filter(parent__type=RecordTypes.INCOME),
                                          required=False)

    def clean_type(self):
        return RecordTypes.INCOME
