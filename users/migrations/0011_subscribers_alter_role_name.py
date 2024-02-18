# Generated by Django 5.0.1 on 2024-02-16 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_user_email_alter_user_first_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscribers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(error_messages={'unique': 'A subscriber with that email already exists.'}, max_length=254, unique=True, verbose_name='email address')),
            ],
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(error_messages={'unique': 'This role already exists.'}, max_length=255, unique=True),
        ),
    ]