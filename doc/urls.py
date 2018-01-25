#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2018/1/22 上午6:42
# @Author  : MiracleYoung
# @File    : urls.py

from django.conf.urls import url, include
from . import views

mo_url_patterns = [
    url(r'^list/', views.DocMOListView.as_view(), name='list', kwargs={'path2': 'List'}),
    url(r'^deploy/', include([
        url(r'^exec-cmd/$', views.DocDeployExecCmdView.as_view(), name='exec-cmd'),
        url(r'^minion-list/$', views.DocDeployMinionListView.as_view(), name='minion-list'),
    ], namespace='deploy'), kwargs={'path2': 'Deploy'}),
    url(r'^ssh/', views.DocSSHView.as_view(), name='ssh', kwargs={'path2': 'SSH'}),
]

urlpatterns = [
    url(r'^mo/', include(mo_url_patterns, namespace='mo'), kwargs={'path1': 'MO'})

]
