# Generated by Django 5.0.1 on 2024-02-16 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_product_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='availability',
        ),
    ]
