# Generated by Django 4.2.1 on 2023-06-16 14:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_exchanges", "0018_exchanges_currencies_new_currency"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="exchanges_commodities",
            name="unit_int_value",
        ),
        migrations.RemoveField(
            model_name="exchanges_commodities",
            name="unit_str_value",
        ),
        migrations.AddField(
            model_name="commodity",
            name="unit_int_value",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="commodity",
            name="unit_str_value",
            field=models.CharField(max_length=50, null=True),
        ),
    ]
