# Generated by Django 4.1.5 on 2023-01-26 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace_main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]