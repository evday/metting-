#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2017-12-10,9:28"

from django.forms import ModelForm,fields
from django.forms import widgets as wid
from django.core.exceptions import ValidationError

from room import models

class RegisterForm(ModelForm):

    rep_pwd = fields.CharField(
        error_messages={"required":"密码不能为空"},
        widget=wid.PasswordInput(attrs={"class":"form-control","placeholder":"请再次输入密码"})

    )
    class Meta:
        model=models.User
        fields = "__all__"

        error_messages = {
            "phone":{"required":"手机号不能为空","invalid":"请输入正确的手机号"},
            "user":{"required":"用户名不能为空"},
            "pwd":{"required":"密码不能为空"},

        }

        widgets = {
            "phone":wid.TextInput(attrs={"class":"form-control","placeholder":"手机号"}),
            "user":wid.TextInput(attrs={"class":"form-control","placeholder":"用户名"}),
            "pwd":wid.PasswordInput(attrs={"class":"form-control","placeholder":"密码"}),

        }
    def clean(self):
        password = self.cleaned_data.get("pwd")
        repeat_password = self.cleaned_data.get("rep_pwd")
        if password == repeat_password:
            return self.cleaned_data
        else:
            raise ValidationError("两次输入的密码不一致")



