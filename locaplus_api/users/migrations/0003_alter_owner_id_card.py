# Generated by Django 5.0.1 on 2024-01-26 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_user_object_customer_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='id_card',
            field=models.ImageField(blank=True, upload_to='users/owners/id_card/%Y/%m/%d/'),
        ),
    ]
