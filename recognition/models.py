from django.db import models

from user.models import User


class Detection(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, default='', null=False)
    time = models.CharField('time', max_length=32, null=False)
    number = models.BigIntegerField('number', null=False)
    camera_url = models.CharField('camera_url', max_length=256, null=False)
    path = models.CharField('path', max_length=128, null=False)
