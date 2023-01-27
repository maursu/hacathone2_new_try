# Generated by Django 4.1.5 on 2023-01-27 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace_main', '0005_alter_stuffs_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stuffs',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stuffs', to='marketplace_main.category'),
        ),
    ]
