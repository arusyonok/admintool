# Generated by Django 4.1.1 on 2022-10-07 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('type', models.IntegerField(choices=[(0, 'Expense'), (1, 'Income'), (2, 'Transfer')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.category')),
            ],
        ),
    ]
