# Generated by Django 5.1.5 on 2025-03-03 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poker', '0011_alter_bot_bot_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='new_field',
        ),
        migrations.AddField(
            model_name='bot',
            name='name',
            field=models.CharField(default=1, max_length=140),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(default=1, max_length=140),
            preserve_default=False,
        ),
    ]
