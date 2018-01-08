#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2018/1/6 上午7:55
# @Author  : MiracleYoung
# @File    : mixin.py

from django.shortcuts import redirect, reverse, HttpResponseRedirect
from django.conf import settings
# from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from user.models.user import User


class LoginRequiredMixin:

    def dispatch(self, request, *args, **kwargs):

        if request.session.get('uid') and request.session.get('token') and request.session.get('token_exp'):
            # if auto login success, update exp time
            request.session['token_exp'] = (datetime.datetime.now() + datetime.timedelta(days=7)).timestamp()
            # add user avatar
            try:
                u = User.objects.get(pk=request.session.get('uid'))
            except User.DoesNotExist:
                raise self.form.add_error('user', 'User is incorrect.')
            context =  self.get_context_data(**kwargs)
            context['user'] = u
            kwargs.update(context)
            return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
        else:
            redirect_url = self.retrieve_redirect_url(request.path)
            return redirect(redirect_url)

    def retrieve_redirect_url(self, path, login_url=settings.LOGIN_URL):
        _login_url = reverse(login_url)
        return '%s?next=%s' % (_login_url, path)
        