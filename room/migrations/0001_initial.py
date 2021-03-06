# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-10 04:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(max_length=32, verbose_name='预定时间')),
            ],
            options={
                'verbose_name_plural': '订单表',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='会议室标题')),
            ],
            options={
                'verbose_name_plural': '会议室',
            },
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=16, verbose_name='时间段')),
            ],
            options={
                'verbose_name_plural': '时刻表',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=32, verbose_name='用户名')),
                ('pwd', models.CharField(max_length=16, verbose_name='密码')),
                ('phone', models.IntegerField(verbose_name='手机号')),
            ],
            options={
                'verbose_name_plural': '用户表',
            },
        ),
        migrations.AddField(
            model_name='room',
            name='time',
            field=models.ManyToManyField(to='room.Time', verbose_name='开放时间'),
        ),
        migrations.AddField(
            model_name='order',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room.Room', verbose_name='预定的会议室'),
        ),
        migrations.AddField(
            model_name='order',
            name='time',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room.Time', verbose_name='预定时间段'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room.User', verbose_name='联系人'),
        ),
        migrations.AlterUniqueTogether(
            name='order',
            unique_together=set([('room', 'day', 'time')]),
        ),
    ]
