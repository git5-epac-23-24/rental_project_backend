# Generated by Django 5.0.1 on 2024-02-14 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_rent_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='availability',
            field=models.CharField(max_length=255),
        ),
    ]
