# Generated by Django 4.1.5 on 2023-01-23 14:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('title', models.CharField(max_length=30, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=30, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Stuffs',
            fields=[
                ('title', models.CharField(max_length=30)),
                ('descriptinon', models.TextField()),
                ('image', models.ImageField(blank=True, upload_to='stuffs_image/')),
                ('slug', models.SlugField(blank=True, max_length=30, primary_key=True, serialize=False)),
                ('posted_at', models.DateField(auto_now_add=True)),
                ('price', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stuffs', to='marketplace_main.category')),
            ],
            options={
                'verbose_name': 'Stuff',
                'verbose_name_plural': 'Stuffs',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to=settings.AUTH_USER_MODEL)),
                ('stuff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='marketplace_main.stuffs')),
            ],
            options={
                'verbose_name': 'Rating',
                'verbose_name_plural': 'Rating',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('posted_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('stuff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='marketplace_main.stuffs')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Commentaries',
            },
        ),
    ]
