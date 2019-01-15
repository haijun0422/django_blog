# -*- coding: utf-8 -*-
# @Time    : 19-1-11 下午5:22
# @Author  : Nick
# @Email   : haijun0422@126.com
# @File    : forms.py
# @Software: PyCharm

from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        exclude = ['author', 'views', 'slug', 'pub_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.CheckboxSelectMultiple(attrs={'class': 'multi-checkbox'}),
        }