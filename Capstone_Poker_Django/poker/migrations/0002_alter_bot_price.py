# Generated by Django 4.2.11 on 2025-02-25 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot',
            name='price',
            field=models.DecimalField(decimal_places=3, max_digits=5),
        ),
    ]
