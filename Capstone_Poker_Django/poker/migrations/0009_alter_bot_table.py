# Generated by Django 5.1.5 on 2025-03-02 23:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poker', '0008_rename_char_field_bot_bot_name_remove_bot_text_field'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='bot',
            table='PokerBots',
        ),
    ]
