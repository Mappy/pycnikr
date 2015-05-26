# -*- coding: utf-8 -*-
from os.path import join, dirname
import tempfile

from django.shortcuts import render
from django.http import HttpResponse

from pycnik import pycnik

def template(request, name):
    name = name if name.endswith('.py') else name + '.py'
    stylesheets_dir = join(dirname(__file__), 'stylesheets')
    stylesheet = open(join(stylesheets_dir, name), 'r')
    content = stylesheet.read()

    return render(
        request, 'main_app/index.html',
        {
            "name": name[:-3],
            'stylesheet_content': content,
        }
    )

def pycnik_handler(request, stylesheet):
    tmp_dir = tempfile.gettempdir()
    py_stylesheet_path = join(tmp_dir, stylesheet + '.py')
    with open(py_stylesheet_path, 'w') as f:
       f.write(request.body)
    py_stylesheet = pycnik.import_style(py_stylesheet_path)
    pycnik.translate(py_stylesheet, join(tmp_dir, stylesheet + '.xml'))
    return HttpResponse('Stylesheet successfully applied')
