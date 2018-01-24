#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/18/18 11:07 AM
# @Author  : Miracle Young
# @File    : api.py

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import json, os
from .models import *
from .saltapi import SaltAPI
from asset.models import Server

SALT_API_URL = settings.SALT_API_URL
SALT_API_USERNAME = settings.SALT_API_USERNAME
SALT_API_PASSWORD = settings.SALT_API_PASSWORD


def init_server(saltapi, hostname):
    _payload = saltapi.remote_one_server(hostname, 'grains.items')
    _disk = saltapi.remote_one_server(hostname, 'status.diskusage')
    _server_info = {}
    _server_info['disk'] = json.dumps(_disk)
    _server_info['cpu'] = int(_payload['num_cpus']) * int(_payload['num_cpus'])
    _server_info['memory'] = round(int(_payload['mem_total']) / 1024)
    _server_info['os'] = _payload['os'] + _payload['osrelease']
    _server_info['os_arch'] = _payload['osarch']
    _server_info['hostname'] = hostname
    _server_info['public_ip'] = _payload['ipv4'][1]
    _server_info['sn'] = _payload['serialnumber']
    try:
        type_env, biz, _ = hostname.split('.')
        type, env = type_env.split('-')
        if type == 'web':
            _server_info['type'] = 1
        elif type == 'db':
            _server_info['type'] = 2
        elif type == 'big':
            _server_info['type'] = 3
        elif type == 'mid':
            _server_info['type'] = 4
        elif type == 'dev':
            _server_info['type'] = 5
        else:
            _server_info['type'] = 99

        if env == 'pro':
            _server_info['env'] = 1
        elif env == 'gl':
            _server_info['env'] = 2
        elif env == 'stg':
            _server_info['env'] = 3
        elif env == 'dev':
            _server_info['env'] = 4
        elif env == 'test':
            _server_info['env'] = 5
    except:
        biz, _ = hostname.split('.')
        _server_info['type'] = 99
        _server_info['env'] = 99

    _server_info['remark'] = biz
    _server_info['hardware_version'] = _payload['manufacturer']
    _server_info['uuid'] = _payload['uuid']
    _server = Server(**_server_info)
    _server.save()
    return _server


class MinionRefreshApi(APIView):
    def get(self, request, **kwargs):
        _saltapi = SaltAPI(url=SALT_API_URL, username=SALT_API_USERNAME, password=SALT_API_PASSWORD)
        _minions = _saltapi.list_all_key()[0]
        _minions_pre = _saltapi.list_all_key()[1]


install
for _minion in _minions:
    if not SaltMinion.objects.filter(hostname=_minion):
        _salt_minion = SaltMinion(hostname=_minion, status=1, is_alive=False)
        # retrieve server info and initial it
        _salt_minion.server = init_server(_saltapi, _minion)
        _salt_minion.save()
    else:
        SaltMinion.objects.filter(hostname=_minion).update(status=1, is_alive=False)
for _minion in _minions_pre:
    if not SaltMinion.objects.filter(hostname=_minion):
        SaltMinion.objects.create(hostname=_minion, status=2, is_alive=False)
    else:
        SaltMinion.objects.filter(hostname=_minion).update(status=2, is_alive=False)

return Response('success', status=status.HTTP_200_OK)


class MinionCheckAliveApi(APIView):
    def get(self, request):
        _saltapi = SaltAPI(url=SALT_API_URL, username=SALT_API_USERNAME, password=SALT_API_PASSWORD)
        _ret = _saltapi.salt_check_alive('*')
        for host, is_alive in _ret.items():
            SaltMinion.objects.filter(hostname=host).update(is_alive=is_alive, last_alive_time=timezone.now(),
                                                            update_time=timezone.now())
        return Response('success')


class MinionApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = SaltMinion

    def delete(self, request, *args, **kwargs):
        _saltapi = SaltAPI(url=SALT_API_URL, username=SALT_API_USERNAME, password=SALT_API_PASSWORD)
        pk = kwargs.get('pk')
        try:
            _minion = SaltMinion.objects.get(id=pk)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        _ret = _saltapi.delete_key(_minion.hostname)
        if _ret:
            SaltMinion.objects.filter(hostname=_minion.hostname).update(is_alive=False, status=5)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        _saltapi = SaltAPI(url=SALT_API_URL, username=SALT_API_USERNAME, password=SALT_API_PASSWORD)
        pk = kwargs.get('pk')
        try:
            _minion = SaltMinion.objects.get(id=pk)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        _ret = _saltapi.accept_key(_minion.hostname)
        if _ret:
            _minion.status = 1
            _minion.server = init_server(_saltapi, _minion.hostname)
            _minion.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ExecuteCommandApi(APIView):

    def post(self, request, *args, **kwargs):
        _type = request.data.get('type', '')
        if _type == 'glob':
            _server = request.data.get('servers', '')
        elif _type == 'list':
            _server = request.data.getlist('servers[]', '')
        _cmds = request.data.getlist('cmds[]', '')
        _raw_args = request.data.getlist('args[]', [])
        _args = [_arg.split(',') for _arg in _raw_args]
        _saltapi = SaltAPI(url=SALT_API_URL, username=SALT_API_USERNAME, password=SALT_API_PASSWORD)
        _payload = _saltapi.remote_execution(_server, _cmds, tgt_type=_type, arg=_args)
        return Response(_payload, status=status.HTTP_200_OK)


class RosterApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Roster

    def get(self, request, *args, **kwargs):
        _pk = kwargs.get('pk', -1)
        try:
            _roster = Roster.objects.get(pk=_pk)
        except ObjectDoesNotExist:
            raise Response('roster does not exist', status=status.HTTP_404_NOT_FOUND)
        with open(_roster.file.path, 'r') as f:
            _content = f.read()
        return Response(_content.replace('\n', '<br>').replace(' ', '&nbsp;' * 2), status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        _pk = kwargs.get('pk', -1)
        try:
            _roster = Roster.objects.get(pk=_pk)
        except ObjectDoesNotExist:
            raise Response('roster does not exist', status=status.HTTP_404_NOT_FOUND)
        _roster.status = 2
        _roster.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class InstallMinionApi(APIView):
    def get(self, request, *args, **kwargs):
        _pk = self.kwargs.get('roster_id', -1)
        try:
            _roster = Roster.objects.get(pk=_pk)
        except ObjectDoesNotExist:
            raise Response('roster does not exist', status=status.HTTP_400_BAD_REQUEST)
        # create symbol link from roster to /etc/salt/roster
        _filepath = _roster.file.path
        _rosterpath = '/etc/salt/roster'
        if os.path.exists(_rosterpath):
            os.remove(_rosterpath)
        os.symlink(_filepath, _rosterpath)
        _saltapi = SaltAPI(url=SALT_API_URL, username=SALT_API_USERNAME, password=SALT_API_PASSWORD)
        _fun = ['cmd.run', ]
        _arg = [['curl -L https://bootstrap.saltstack.com -o install_salt.sh', 'sudo sh install_salt.sh', ], ]
        _payload = _saltapi.remote_execution(tgt='*', fun=_fun, arg=_arg, client='ssh')
        return Response(_payload, status=status.HTTP_200_OK)
