# Generated by Django 5.0 on 2024-01-05 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0037_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('CZ', 'Cheese'), ('PN', 'Paneer'), ('MS', 'Milk Shake'), ('LS', 'Lassi'), ('IC', 'Ice-Cream'), ('CR', 'Curd'), ('ML', 'Milk'), ('GH', 'Ghee')], max_length=2),
        ),
    ]
