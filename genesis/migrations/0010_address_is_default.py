# Generated by Django 3.2.3 on 2021-05-31 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genesis', '0009_auto_20210528_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
    ]