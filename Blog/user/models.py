from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserProfile(AbstractUser):
    mobile=models.CharField(max_length=11,verbose_name='手机号码',unique=True)
    icon=models.ImageField(upload_to='uploads/%Y/%m/%d')
    yunicon=models.CharField(max_length=200,default='')

    class Meta:
        db_table='UserProfile'
        verbose_name='用户表'
        verbose_name_plural=verbose_name
