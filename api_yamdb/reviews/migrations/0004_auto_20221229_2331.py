# Generated by Django 3.2 on 2022-12-29 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_alter_review_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]