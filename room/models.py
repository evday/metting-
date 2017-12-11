from django.db import models

# Create your models here.

class User(models.Model):
    user = models.CharField(max_length=32,verbose_name="用户名")
    pwd = models.CharField(max_length=16,verbose_name="密码")
    phone = models.IntegerField(verbose_name="手机号")

    class Meta:
        verbose_name_plural = "用户表"

    def __str__(self):
        return self.user

class Room(models.Model):
    name = models.CharField(max_length=32,verbose_name="会议室标题")
    time = models.ManyToManyField(to="Time",verbose_name="开放时间")

    class Meta:
        verbose_name_plural = "会议室"

    def __str__(self):
        return self.name

class Time(models.Model):

    title = models.CharField(max_length=16,verbose_name="时间段")

    class Meta:
        verbose_name_plural = "时刻表"

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(to='User',verbose_name="联系人")
    room = models.ForeignKey(to="Room",verbose_name="预定的会议室")
    day = models.DateField(max_length=32,verbose_name="预定时间")
    time = models.ForeignKey(to="Time",verbose_name="预定时间段")



    class Meta:
        unique_together = ("room","day","time")
        verbose_name_plural = "订单表"

    def __str__(self):
        return self.user
