# -*- coding: utf-8 -*-

from django.conf.urls import url
from main_app.views import template

urlpatterns = [
    url(r'save/(.*)', 'main_app.views.save'),
    url(r'preview/(.*)', 'main_app.views.preview'),
    url(r'(.*)', 'main_app.views.template'),
]
