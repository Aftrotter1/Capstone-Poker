from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from anchor.models.fields import SingleAttachmentField
from PIL import Image
from django.core.validators import MinValueValidator

class BaseBot(models.Model):
    name = models.CharField(max_length=140)
    Bot_File = models.FileField(upload_to="")
    
    class Meta:
        db_table = 'BasePokerBots'

class StudentBot(models.Model):
    name = models.CharField(max_length=140)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Bot_File = models.FileField(upload_to="")
    uploaded_at= models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'StudentPokerBots'

class Tournament(models.Model):
    StudentID = models.ForeignKey(User, on_delete=models.CASCADE)
    BotID = models.ForeignKey(StudentBot, on_delete=models.CASCADE)
    NumberOfRounds=models.IntegerField()
    NumberOfWins=models.IntegerField()
    
    class Meta:
        db_table = 'Tournament'

class TournamentData(models.Model):
    DateRun= models.DateField(auto_now_add=True)
    Notes= models.CharField(max_length=140)
    NumberofPlayers=models.IntegerField()
    NumberofGames=models.IntegerField()
    Visible = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'TournamentData'

class Profile(models.Model):
    name = models.CharField(max_length=140)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        # Call the original save() method
        super().save(*args, **kwargs)

        # Now resize the avatar if it exists
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 100 or img.width > 100:
                new_size = (100, 100)
                img.thumbnail(new_size)
                img.save(self.avatar.path)
