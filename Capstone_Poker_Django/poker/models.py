from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from anchor.models.fields import SingleAttachmentField

class Bot(models.Model):
    name = models.CharField(max_length=140)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Bot_File = models.FileField(upload_to="")
    uploaded_at= models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'PokerBots'



# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    name = models.CharField(max_length=140)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
from PIL import Image

# resizing images
def save(self, *args, **kwargs):
    super().save()

    img = Image.open(self.avatar.path)

    if img.height > 100 or img.width > 100:
        new_img = (100, 100)
        img.thumbnail(new_img)
        img.save(self.avatar.path)