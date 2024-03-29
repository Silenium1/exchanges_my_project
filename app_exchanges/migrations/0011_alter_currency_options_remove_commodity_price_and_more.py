# Generated by Django 4.2.1 on 2023-06-15 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_exchanges', '0010_delete_asset_class'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='currency',
            options={},
        ),
        migrations.RemoveField(
            model_name='commodity',
            name='price',
        ),
        migrations.RemoveField(
            model_name='commodity',
            name='time_of_last_trade',
        ),
        migrations.RemoveField(
            model_name='commodity',
            name='unit_int_value',
        ),
        migrations.RemoveField(
            model_name='commodity',
            name='unit_str_value',
        ),
        migrations.RemoveField(
            model_name='currency',
            name='base_currency',
        ),
        migrations.RemoveField(
            model_name='currency',
            name='price',
        ),
        migrations.RemoveField(
            model_name='currency',
            name='type',
        ),
        migrations.AddField(
            model_name='commodity',
            name='commodity_name',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='currency',
            name='currency_name',
            field=models.CharField(default='test', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='currency',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Exchanges_Currencies',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('SPOT', 'SPOT'), ('FORWARD', 'FORWARD'), ('SWAP', 'SWAP')], default='SPOT', max_length=15)),
                ('base_currency', models.CharField(choices=[('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP')], default='USD', max_length=15)),
                ('tenor_months', models.CharField(blank=True, choices=[('1 M', '1 M'), ('2 M', '2 M'), ('3 M', '3 M')], max_length=15)),
                ('settlement_date', models.DateTimeField(blank=True, null=True)),
                ('settlement_date_swap', models.DateTimeField(blank=True, null=True)),
                ('price', models.IntegerField()),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_exchanges.currency')),
                ('exchange', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_exchanges.exchange')),
            ],
        ),
        migrations.CreateModel(
            name='Exchanges_Commodities',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('unit_int_value', models.IntegerField()),
                ('unit_str_value', models.CharField(max_length=50)),
                ('time_of_last_trade', models.CharField(max_length=50, null=True)),
                ('price', models.IntegerField()),
                ('commodity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_exchanges.commodity')),
                ('exchange', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_exchanges.exchange')),
            ],
        ),
    ]
