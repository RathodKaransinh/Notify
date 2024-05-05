from django.db import models
import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.

class NoticeKeyword(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Notice(models.Model):
    title = models.CharField(max_length=50)
    short_description = models.TextField(default='', blank=True, max_length=255)
    datetime = models.DateTimeField(default=datetime.datetime.now)
    file = models.FileField(upload_to='static')
    keywords = models.ManyToManyField(NoticeKeyword, verbose_name='Notice Keywords')

    def __str__(self):
        return self.title
    

class Item(models.Model):
    title = models.CharField(max_length=50)
    keyword = models.ForeignKey(NoticeKeyword, verbose_name='Notice Keywords', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.title


@receiver(post_save, sender=Notice)
def send_email(sender, instance, **kwargs):
    to_list_of_tuple = list(User.objects.values_list('email'))
    to_list = []
    for item in to_list_of_tuple:
        to_list.append(item[0])
    mail = EmailMessage(f'Notice: {instance.title}', instance.short_description, settings.EMAIL_HOST_USER, to_list)
    mail.attach_file(str(instance.file))
    mail.send()
