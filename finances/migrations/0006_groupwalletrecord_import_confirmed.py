# Generated by Django 4.1.2 on 2022-12-21 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0005_groupwalletrecord_tags_personalwalletrecord_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupwalletrecord',
            name='import_confirmed',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='personalwalletrecord',
            name='import_confirmed',
            field=models.BooleanField(default=True),
        ),
    ]
