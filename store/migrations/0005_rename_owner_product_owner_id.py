# Generated by Django 5.0.1 on 2024-02-23 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_merge_20240223_1745'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='owner',
            new_name='owner_id',
        ),
    ]