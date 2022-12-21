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
    wallet_id = forms.ChoiceField(choices=[])
    delimiter = forms.ChoiceField(choices=DELIMITER_CHOICES)
    import_origin = forms.ChoiceField(choices=ImportOrigin.CHOICES)

    def __init__(self, wallets=(), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['wallet_id'].choices = ((wallet.id, wallet.title) for wallet in wallets)

    def clean(self):
        cleaned_data = super().clean()
        clean_wallet_id = cleaned_data["wallet_id"]
        try:
            wallet = Wallet.objects.get(id=clean_wallet_id)
        except Wallet.DoesNotExist:
            raise ValidationError("Selected wallet does not exist!")

        clean_import_origin = int(cleaned_data["import_origin"])
        if wallet.is_personal_wallet and clean_import_origin != ImportOrigin.NORDEA:
            raise ValidationError("Personal Wallet works only with Nordea as import origin")

        if wallet.is_group_wallet and clean_import_origin != ImportOrigin.TRICOUNT:
            raise ValidationError("Group Wallet works only with Tricount as import origin")

        return cleaned_data
