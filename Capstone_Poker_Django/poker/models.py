from django.db import models

# Create your models here.

from django.db import models

class Bot(models.Model):
    char_field = models.CharField(max_length=255)
    text_field = models.TextField()
    
    class Bots:
        db_table = 'PokerBots'