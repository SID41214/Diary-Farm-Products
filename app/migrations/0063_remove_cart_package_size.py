# Generated by Django 5.0 on 2024-01-15 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0062_cart_package_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='package_size',
        ),
    ]