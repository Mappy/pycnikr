# -*- coding: utf-8 -*-

from django.conf.urls import url

urlpatterns = [
    url(r'save/(.*)', 'pycnikr.views.save'),
    url(r'preview/(.*)', 'pycnikr.views.preview'),
    url(r'(.+)', 'pycnikr.views.edit'),
    url(r'', 'pycnikr.views.home'),
]
