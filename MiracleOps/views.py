#!/usr/bin/env python
# encoding: utf-8
# @Time    : 1/2/2018 5:00 PM
# @Author  : Miracle Young
# @File    : views.py

from django.views.generic.base import TemplateView
from common.mixin import LoginRequiredMixin

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"


class TestLongUrlView(LoginRequiredMixin, TemplateView):
    template_name = 'test_long_url.html'