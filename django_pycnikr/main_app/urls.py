# -*- coding: utf-8 -*-

from django.conf.urls import url
from main_app.views import template

urlpatterns = [
    url(r'save/(.*)', 'main_app.views.save'),
    url(r'apply/(.*)', 'main_app.views.apply'),
    url(r'(.*)', 'main_app.views.template'),
]
