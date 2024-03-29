# Generated by Django 4.2.1 on 2023-06-19 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_exchanges', '0021_remove_exchanges_currencies_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchanges_commodities',
            name='time_of_last_trade',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='exchanges_currencies',
            name='settlement_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='exchanges_currencies',
            name='settlement_date_swap',
            field=models.DateField(blank=True, null=True),
        ),
    ]
