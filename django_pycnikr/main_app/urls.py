# -*- coding: utf-8 -*-

from django.conf.urls import url
from main_app.views import template

urlpatterns = [
    url(r'save/(.*)', 'main_app.views.save_template'),
    url(r'pycnik/(.*)', 'main_app.views.pycnik_handler'),
    url(r'(.*)', 'main_app.views.template'),
]
