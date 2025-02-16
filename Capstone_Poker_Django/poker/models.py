from django.db import models

# Create your models here.

class Bot(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    specs = models.FileField(upload_to="poker")