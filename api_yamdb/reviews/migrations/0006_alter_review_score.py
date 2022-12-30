# Generated by Django 3.2 on 2022-12-30 11:12

import reviews.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_alter_review_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.IntegerField(default=0, validators=[reviews.models.Review.validate_interval]),
        ),
    ]