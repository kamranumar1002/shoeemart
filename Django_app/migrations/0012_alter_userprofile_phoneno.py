# Generated by Django 3.2 on 2021-10-23 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Django_app', '0011_shippingaddress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='PhoneNo',
            field=models.IntegerField(null=True),
        ),
    ]
