from django.db import models

from user.models import User


class Intrusion(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, default='', null=False)
    intrusion_time = models.CharField('入侵时间', max_length=32, null=False)
    video_path = models.CharField('视频路径', max_length=128, null=False)
