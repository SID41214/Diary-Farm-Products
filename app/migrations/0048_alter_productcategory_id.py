# Generated by Django 5.0 on 2024-01-08 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0047_alter_productcategory_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategory',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
