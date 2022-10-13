from django import forms
from authorization.models import User
from catalog.models import Category, SubCategory
from catalog.common import RecordTypes
from .models import PersonalRecord


class PersonalRecordCreateForm(forms.ModelForm):
    type = forms.CharField(widget=forms.HiddenInput(), required=False)
    user = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = PersonalRecord
        fields = ["title", "amount", "type", "sub_category", "user"]

    def clean_user(self):
        return User.objects.first()


class ExpenseCreateForm(PersonalRecordCreateForm):
    sub_category = forms.ModelChoiceField(queryset=SubCategory.objects.filter(parent__type=RecordTypes.EXPENSE),
                                          required=False)

    def clean_type(self):
        return RecordTypes.EXPENSE


class PersonalRecordUpdateForm(forms.ModelForm):
    type = forms.CharField(widget=forms.HiddenInput(), required=False)
    user = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = PersonalRecord
        fields = ["title", "amount", "type", "sub_category", "user"]

    def clean_user(self):
        return User.objects.first()


class ExpenseUpdateForm(PersonalRecordUpdateForm):
    sub_category = forms.ModelChoiceField(queryset=SubCategory.objects.filter(parent__type=RecordTypes.EXPENSE),
                                          required=False)

    def clean_type(self):
        return RecordTypes.EXPENSE
