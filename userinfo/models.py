from django.contrib.auth.models import User
from django.db import models


# Create your models here.

# 用户信息
class user_info_data(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=14, blank=True)
    age = models.CharField(max_length=5, blank=True)
    sex = models.CharField(max_length=10, blank=True)
    background_img = models.ImageField(upload_to='background_img/%Y%m%d/', blank=True)
    portrait = models.ImageField(upload_to='portrait/%Y%m%d/', blank=True)
    self_introduce = models.TextField(max_length=500, blank=True)
    signature = models.TextField(max_length=500, blank=True)


# 关注表
class Follow(models.Model):
    follow = models.ForeignKey(User, related_name="follow_user", on_delete=models.CASCADE, blank=True, null=True)
    fan = models.ForeignKey(User, related_name="fan_user", on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, related_name="myself", on_delete=models.CASCADE, blank=True, null=True)
