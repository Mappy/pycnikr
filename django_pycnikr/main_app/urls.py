# -*- coding: utf-8 -*-

from django.conf.urls import url
from main_app.views import template

urlpatterns = [
    url(r'pycnik/(.*)', 'main_app.views.pycnik'),
    url(r'(.*)', 'main_app.views.template'),
]
