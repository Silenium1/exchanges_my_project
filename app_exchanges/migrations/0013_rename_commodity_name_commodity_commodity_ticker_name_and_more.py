# Generated by Django 4.2.1 on 2023-06-16 00:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_exchanges', '0012_alter_currency_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commodity',
            old_name='commodity_name',
            new_name='commodity_ticker_name',
        ),
        migrations.RenameField(
            model_name='currency',
            old_name='currency_name',
            new_name='currency_ticker_name',
        ),
    ]
