#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2018/1/6 上午7:55
# @Author  : MiracleYoung
# @File    : mixins.py

from rest_framework import response
from django.shortcuts import redirect, reverse
from django.conf import settings

from users.models import User, Token


class JsonResponseMixin:
    def json_response(self, code, data, msg):
        return response.Response(status=code, data={'code': code, 'data': data, 'msg': msg},
                                 content_type='application/json')


class CookieMixin:
    def __init__(self):
        self._cookies = []

    def get_cookies(self):
        return self._cookies

    def add_cookie(self, **kwargs):
        self._cookies.append(kwargs)

    def dispatch(self, request, *args, **kwargs):
        _res = super(CookieMixin, self).dispatch(request, *args, **kwargs)
        for _item in self.get_cookies():
            _res.set_cookie(**_item)
        return _res


class LoginRequiredMixin(CookieMixin, JsonResponseMixin):
    def dispatch(self, request, *args, **kwargs):
        _token = request.META.get('HTTP_X_ACCESS_TOKEN', '') or request.COOKIES.get('jwt', '')
        _ret, _payload = Token.verify_token(_token)
        if _ret:
            try:
                _t = Token.objects.get(token=_token)
            except Token.DoesNotExist:
                return self._res_token_error(request)
            else:
                # prevent cookie exp time updated by others.
                if Token.token_is_expire(_t):
                    return self._res_token_error(request)

                if hasattr(request, 'user'):
                    request.user = User.objects.get(id=_payload.get('iss'))

                return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
        else:
            return self._res_token_error(request)

    def retrieve_redirect_url(self, path, login_url=settings.LOGIN_URL):
        _login_url = reverse(login_url)
        return '{}?next={}'.format(_login_url, path)

    def _res_token_error(self, request):
        if request.is_ajax():
            return self.json_response(1003, '', 'token error.')
        else:
            return redirect(self.retrieve_redirect_url(request.path))


class GetHtmlPrefixMixin:
    def get_html_prefix(self, **kwargs):
        _html_name = self.request.path.replace('-', '_').split('/')
        _html_name.pop(0)
        _html_name.pop()
        _html_prefix = '_'.join(_html_name)
        return _html_prefix

    def get_context_data(self, **kwargs):
        kwargs['html_prefix'] = 'md/' + self.get_html_prefix() + '.md'
        return kwargs
