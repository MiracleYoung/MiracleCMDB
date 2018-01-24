#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2018/1/9 下午10:13
# @Author  : MiracleYoung
# @File    : entity.py

from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from asset.serializer import *
from asset.models import *

__all__ = ['ServerApi', 'IDCApi']


class ServerApi(RetrieveUpdateDestroyAPIView):
    serializer_class = ServerSerializer

    def delete(self, request, *args, **kwargs):
        queryset = Server.objects.filter(pk=kwargs.get('pk', ''))
        try:
            queryset.update(status=2)
            return Response('', status=status.HTTP_204_NO_CONTENT)
        except:
            return Response('', status=status.HTTP_502_BAD_GATEWAY)


class IDCApi(RetrieveUpdateDestroyAPIView):
    serializer_class = IDCSerializer

    def delete(self, request, *args, **kwargs):
        queryset = IDC.objects.filter(pk=kwargs.get('pk', ''))
        try:
            queryset.update(status=2)
            return Response('', status=status.HTTP_204_NO_CONTENT)
        except:
            return Response('', status=status.HTTP_502_BAD_GATEWAY)
