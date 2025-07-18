from django.db import models

# Create your models here.
class KeyboardNum(models.Model):
    Workername = models.CharField(max_length=200)
    SN =  models.CharField(max_length=200)
    Time = models.DateTimeField(auto_now_add=True)
    