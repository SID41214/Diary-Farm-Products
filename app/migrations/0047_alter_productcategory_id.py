# Generated by Django 5.0 on 2024-01-06 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0046_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategory',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]