# Generated by Django 4.2.1 on 2023-06-06 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_exchanges', '0005_alter_currency_base_currency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commodity',
            name='id_asset_class',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app_exchanges.asset_class'),
        ),
        migrations.AlterField(
            model_name='currency',
            name='id_asset_class',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='app_exchanges.asset_class'),
        ),
        migrations.AlterField(
            model_name='currency',
            name='settlement_date',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='currency',
            name='settlement_date_swap',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='ticker',
            name='ticker_name',
            field=models.CharField(max_length=50),
        ),
    ]
