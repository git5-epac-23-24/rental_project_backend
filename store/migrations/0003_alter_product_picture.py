# Generated by Django 5.0.1 on 2024-02-23 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_rent_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='products/pictures/%Y/%m/%d/'),
        ),
    ]