from django import forms
from authorization.models import User
from catalog.models import Category, SubCategory
from catalog.common import RecordTypes
from .models import PersonalRecord


class PersonalExpenseCreateForm(forms.ModelForm):
    type = forms.CharField(widget=forms.HiddenInput(), required=False)
    user = forms.CharField(widget=forms.HiddenInput(), required=False)
    sub_category = forms.ModelChoiceField(queryset=SubCategory.objects.filter(parent__type=RecordTypes.EXPENSE),
                                          required=False)

    class Meta:
        model = PersonalRecord
        fields = ["title", "amount", "type", "sub_category", "user"]

    def clean_type(self):
        return RecordTypes.EXPENSE

    def clean_user(self):
        return User.objects.first()
