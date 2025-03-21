# Generated by Django 5.1.5 on 2025-03-21 17:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poker', '0004_rename_tournaments_tournament_alter_tournament_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='TournamentID',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='poker.tournamentdata'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tournamentdata',
            name='NumberofGames',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]
