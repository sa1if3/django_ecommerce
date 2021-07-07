# Generated by Django 3.2.3 on 2021-06-09 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genesis', '0017_alter_ordereditems_item_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('PLACED', 'PLACED'), ('ACCEPTED', 'ACCEPTED'), ('PACKED', 'PACKED'), ('SHIPPED', 'SHIPPED'), ('REJECTED', 'REJECTED'), ('COMPLETED', 'COMPLETED')], max_length=200, null=True),
        ),
    ]