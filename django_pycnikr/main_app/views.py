# -*- coding: utf-8 -*-
from os.path import join, dirname
import tempfile

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from pycnik import pycnik

stylesheets_dir = join(dirname(__file__), 'stylesheets')

@ensure_csrf_cookie
def template(request, name):
    name = name if name.endswith('.py') else name + '.py'
    stylesheet = open(join(stylesheets_dir, name), 'r')
    content = stylesheet.read()
    return render(
        request, 'main_app/index.html',
        {
            'name': name[:-3],
            'stylesheet_content': content,
            'zoom': settings.DEFAULT_ZOOM,
            'center':[settings.DEFAULT_LAT, settings.DEFAULT_LON],
        }
    )

def save(request, name):
    stylesheet_to_save = join(stylesheets_dir, name + '.py')
    with open(stylesheet_to_save, 'w') as fd:
        fd.write(request.body)
    return HttpResponse('Stylesheet successfully saved')

def preview(request, name):
    tmp_dir = tempfile.gettempdir()
    py_stylesheet_path = join(tmp_dir, name + '.py')
    with open(py_stylesheet_path, 'w') as f:
       f.write(request.body)
    py_stylesheet = pycnik.import_style(py_stylesheet_path)
    pycnik.translate(py_stylesheet, join(tmp_dir, name + '.xml'))
    return HttpResponse('Stylesheet successfully applied')

