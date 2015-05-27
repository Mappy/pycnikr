# -*- coding: utf-8 -*-
from os.path import join, dirname
import tempfile

from django.shortcuts import render
from django.http import HttpResponse

from pycnik import pycnik

stylesheets_dir = join(dirname(__file__), 'stylesheets')

def template(request, name):
    print 'toto'
    name = name if name.endswith('.py') else name + '.py'

    print stylesheets_dir
    print join(stylesheets_dir, name)
    stylesheet = open(join(stylesheets_dir, name), 'r')
    content = stylesheet.read()
    return render(
        request, 'main_app/index.html',
        {
            "name": name[:-3],
            'stylesheet_content': content,
        }
    )

def pycnik_handler(request, name):
    tmp_dir = tempfile.gettempdir()
    py_stylesheet_path = join(tmp_dir, name + '.py')
    with open(py_stylesheet_path, 'w') as f:
       f.write(request.body)
    py_stylesheet = pycnik.import_style(py_stylesheet_path)
    pycnik.translate(py_stylesheet, join(tmp_dir, name + '.xml'))
    return HttpResponse('Stylesheet successfully applied')

def save_template(request, name):

    stylesheet_to_save = join(stylesheets_dir, name + '.py')

    with open(stylesheet_to_save, 'w') as fd:
        fd.write(request.body)

    return HttpResponse('Stylesheet successfully saved')

