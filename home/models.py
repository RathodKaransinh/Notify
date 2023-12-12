from django.db import models
import datetime

# Create your models here.

class Notice(models.Model):
    title = models.CharField(max_length=50)
    short_description = models.TextField(default='', blank=True, max_length=255)
    datetime = models.DateTimeField(default = datetime.datetime.now)
    file = models.FileField(upload_to='static')
