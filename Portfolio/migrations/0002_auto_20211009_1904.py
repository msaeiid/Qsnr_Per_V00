# Generated by Django 3.2.7 on 2021-10-09 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='certificate/', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile/', verbose_name='Image'),
        ),
    ]
