# Generated by Django 5.1.5 on 2025-03-02 23:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poker', '0007_remove_profile_avatar_remove_profile_bio_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bot',
            old_name='char_field',
            new_name='Bot_Name',
        ),
        migrations.RemoveField(
            model_name='bot',
            name='text_field',
        ),
    ]
