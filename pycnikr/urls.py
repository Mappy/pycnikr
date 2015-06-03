# -*- coding: utf-8 -*-

from django.conf.urls import url
from pycnikr.views import template
from pycnikr.views import home

urlpatterns = [
    url(r'save/(.*)', 'pycnikr.views.save'),
    url(r'preview/(.*)', 'pycnikr.views.preview'),
    url(r'(.+)', 'pycnikr.views.template'),
    url(r'', 'pycnikr.views.home'),
]