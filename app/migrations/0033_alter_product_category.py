# Generated by Django 5.0 on 2024-01-04 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('PN', 'Paneer'), ('LS', 'Lassi'), ('CZ', 'Cheese'), ('IC', 'Ice-Cream'), ('MS', 'Milk Shake'), ('GH', 'Ghee'), ('ML', 'Milk'), ('CR', 'Curd')], max_length=2),
        ),
    ]