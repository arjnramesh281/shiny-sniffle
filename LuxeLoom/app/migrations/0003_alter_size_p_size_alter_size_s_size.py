# Generated by Django 5.1.4 on 2024-12-12 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_rename_category_product_gender_remove_product_stock_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='size',
            name='p_size',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='size',
            name='s_size',
            field=models.CharField(max_length=10, null=True),
        ),
    ]