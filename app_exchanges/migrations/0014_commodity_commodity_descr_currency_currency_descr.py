# Generated by Django 4.2.1 on 2023-06-16 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_exchanges', '0013_rename_commodity_name_commodity_commodity_ticker_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='commodity',
            name='commodity_descr',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='currency',
            name='currency_descr',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
