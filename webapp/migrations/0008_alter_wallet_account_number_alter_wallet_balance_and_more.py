# Generated by Django 4.2 on 2023-07-03 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_wallet_delete_order_delete_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='account_number',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='balance',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='beneficiary_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='wallet_number',
            field=models.CharField(max_length=50),
        ),
    ]
