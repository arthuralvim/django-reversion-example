# -*- coding: utf-8 -*-

from django import forms
from app1.models import ModelA

class ModelAForm(forms.ModelForm):

    class Meta:
        model = ModelA
        exclude = ('updated_by_user', )
