# Generated by Django 5.0 on 2024-01-06 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0043_product_slug_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('MS', 'Milk Shake'), ('IC', 'Ice-Cream'), ('GH', 'Ghee'), ('ML', 'Milk'), ('LS', 'Lassi'), ('PN', 'Paneer'), ('CR', 'Curd'), ('CZ', 'Cheese')], max_length=2),
        ),
    ]
