# Generated by Django 5.2 on 2025-05-04 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_passwordresetotp_product_productusage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productusage',
            name='prod_quantity',
            field=models.IntegerField(),
        ),
    ]
