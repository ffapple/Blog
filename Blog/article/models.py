from django.db import models
from user.models import UserProfile
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class Tag(models.Model):
    name=models.CharField(max_length=50,verbose_name='标签')

    def __str__(self):
        return self.name
    class Meta:
        db_table='tag'
        verbose_name='标签表'
        verbose_name_plural=verbose_name


class Articel(models.Model):
    title=models.CharField(max_length=100,verbose_name='标题')
    desc=models.CharField(max_length=200,verbose_name='简介')
    content=RichTextUploadingField(verbose_name='内容')
    date=models.DateField(auto_now=True,verbose_name='发表日期')
    click_num=models.IntegerField(default=0,verbose_name='点击量')
    love_num=models.IntegerField(default=0,verbose_name='收藏量')
    image=models.ImageField(upload_to='uploads/article/%Y%m',verbose_name='文章图片',default='uploads/article/202007/p01.jpg')

    # 文章标签是多对多
    tags=models.ManyToManyField(to=Tag)
    user=models.ForeignKey(to=UserProfile,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    class Meta:
        db_table='article'
        verbose_name='文章表'
        verbose_name_plural=verbose_name

class Comment(models.Model):
    nickname=models.CharField(max_length=50,verbose_name='昵称')
    content=models.TextField(verbose_name='内容')
    date=models.DateField(auto_now=True)
    article=models.ForeignKey(to=Articel,verbose_name='文章',on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname
    class Meta:
        db_table='comment'
        verbose_name='评论表'

# 留言表
class Message(models.Model):
    nickname=models.CharField(max_length=50,verbose_name='昵称')
    content=models.TextField(verbose_name='内容')
    date=models.DateField(auto_now=True)
    icon=models.CharField(max_length=160,verbose_name='头像')

    def __str__(self):
        return self.nickname
    class Meta:
        db_table='message'
        verbose_name='留言表'



