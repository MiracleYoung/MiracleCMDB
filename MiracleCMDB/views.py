#!/usr/bin/env python
# encoding: utf-8
# @Time    : 1/2/2018 5:00 PM
# @Author  : Miracle Young
# @File    : views.py

from django.views.generic.base import TemplateView

class IndexView(TemplateView):
    template_name = "index.html"