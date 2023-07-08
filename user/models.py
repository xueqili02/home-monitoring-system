from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField("用户名", max_length=20, null=False)
    password = models.CharField("密码", max_length=18, null=False)
    login_time = models.DateTimeField("登录时间", null=True)
    email = models.CharField("邮箱", max_length=40, null=False)
    camera_urls = models.CharField("摄像头url", max_length=256, default="", null=False)
