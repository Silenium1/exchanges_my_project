# Generated by Django 4.2.1 on 2023-06-14 22:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_exchanges', '0009_remove_commodity_id_asset_class_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Asset_class',
        ),
    ]
