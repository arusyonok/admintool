# Generated by Django 4.1.2 on 2022-12-20 12:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0003_groupwalletrecord_record_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupwalletrecord',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='personalwalletrecord',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
