# Generated by Django 4.2.19 on 2025-02-25 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poker', '0004_rename_bots_bot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bot',
            name='big_integer_field',
        ),
        migrations.RemoveField(
            model_name='bot',
            name='boolean_field',
        ),
        migrations.RemoveField(
            model_name='bot',
            name='date_field',
        ),
        migrations.RemoveField(
            model_name='bot',
            name='date_time_field',
        ),
        migrations.RemoveField(
            model_name='bot',
            name='decimal_field',
        ),
        migrations.RemoveField(
            model_name='bot',
            name='email_field',
        ),
        migrations.RemoveField(
            model_name='bot',
            name='float_field',
        ),
        migrations.RemoveField(
            model_name='bot',
            name='integer_field',
        ),
    ]
