# Generated by Django 3.2.7 on 2021-10-17 06:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portfolio', '0002_auto_20211009_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='point',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)], verbose_name='How much you know about it (1 to 100)'),
        ),
    ]