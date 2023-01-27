# Generated by Django 4.1.5 on 2023-01-27 06:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('marketplace_main', '0003_alter_stuffs_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stuffs',
            name='category',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='stuffs', to='marketplace_main.category'),
        ),
        migrations.AlterField(
            model_name='stuffs',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stuffs', to=settings.AUTH_USER_MODEL),
        ),
    ]
