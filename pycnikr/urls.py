# -*- coding: utf-8 -*-

from django.conf.urls import url
from pycnikr.views import template

urlpatterns = [
    url(r'save/(.*)', 'pycnikr.views.save'),
    url(r'preview/(.*)', 'pycnikr.views.preview'),
    url(r'(.*)', 'pycnikr.views.template'),
]
