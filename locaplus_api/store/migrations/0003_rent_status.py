# Generated by Django 5.0.1 on 2024-02-14 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_remove_rent_customer_product_kitchen_product_length_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rent',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
