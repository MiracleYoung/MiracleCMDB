#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/23/18 2:31 PM
# @Author  : Miracle Young
# @File    : forms.py

from django import forms
from .models import *

__all__ = ['RosterForm', 'SlsForm']

class RosterForm(forms.ModelForm):
    class Meta:
        model = Roster
        fields = '__all__'

class SlsForm(forms.ModelForm):
    class Meta:
        model = Sls
        fields = '__all__'