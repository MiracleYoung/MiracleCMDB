#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2018/1/16 上午7:02
# @Author  : MiracleYoung
# @File    : views_urls.py

from django.conf.urls import url, include
from deploy import views

urlpatterns = [
    url(r'^minion-list/$', views.SaltMinionListView.as_view(), name='minion-list',
        kwargs={'path1': 'Minion List'}),
    url(r'^execute-command/$', views.ExecuteCommandView.as_view(), name='execute-command',
        kwargs={'path1': 'Execute Command'}),
    url(r'^ssh/$', views.SaltSSHView.as_view(), name='ssh', kwargs={'path1': 'SSH'}),
]
