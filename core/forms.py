import os

from django import forms
from django.core.exceptions import ValidationError

from accounts.models import Wallet


class ImportOrigin:
    NORDEA = 0
    TRICOUNT = 1

    CHOICES = (
        (NORDEA, 'Nordea'),
        (TRICOUNT, 'Tricount'),
    )


DELIMITER_CHOICES = ((";", ";"), (",", ","))


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.csv']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class ImportFileUploadForm(forms.Form):
    import_file = forms.FileField(validators=[validate_file_extension])
    wallet = forms.ModelChoiceField(queryset=Wallet.objects.all())
    delimiter = forms.ChoiceField(choices=DELIMITER_CHOICES)
    import_origin = forms.ChoiceField(choices=ImportOrigin.CHOICES)

    def __init__(self, wallets=(), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['wallet'].queryset = wallets

    def clean(self):
        cleaned_data = super().clean()
        wallet = self.cleaned_data['wallet']

        clean_import_origin = int(cleaned_data["import_origin"])
        if wallet.is_personal_wallet and clean_import_origin != ImportOrigin.NORDEA:
            raise ValidationError("Personal Wallet works only with Nordea as import origin")

        if wallet.is_group_wallet and clean_import_origin != ImportOrigin.TRICOUNT:
            raise ValidationError("Group Wallet works only with Tricount as import origin")

        return cleaned_data
