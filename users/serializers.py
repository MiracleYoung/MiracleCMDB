#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2018/1/3 下午9:21
# @Author  : MiracleYoung
# @File    : serializers.py

from rest_framework.serializers import ModelSerializer
from .models import *


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'job_title', 'is_active', 'is_superuser', 'role', 'login_time',]
