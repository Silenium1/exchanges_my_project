# Generated by Django 4.2.1 on 2023-06-18 23:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_exchanges', '0020_currency_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exchanges_currencies',
            name='type',
        ),
    ]
