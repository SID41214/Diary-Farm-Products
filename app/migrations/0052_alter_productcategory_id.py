# Generated by Django 5.0 on 2024-01-09 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0051_productcategory_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategory',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]