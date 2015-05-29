# -*- coding: utf-8 -*-

from os import listdir
from os.path import dirname, join, split, splitext
import tempfile

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from pycnik import pycnik

py_style_sheets_dir = join(dirname(__file__), 'style_sheets')

def select_py_style_sheet(file_path):
    file_dir, file_name = split(file_path)
    file_name, ext = splitext(file_name)
    if ext == '.py':
        return file_name

@ensure_csrf_cookie
def template(request, name):
    py_style_sheets = map(select_py_style_sheet, listdir(py_style_sheets_dir))
    py_style_sheets = filter(lambda x: bool(x) and x != name, py_style_sheets)
    name = name if name.endswith('.py') else name + '.py'
    py_style_sheet = open(join(py_style_sheets_dir, name), 'r')
    py_style_sheet_content = py_style_sheet.read()
    return render(
        request, 'main_app/index.html',
        {
            'style_sheets': py_style_sheets,
            'name': name[:-3],
            'style_sheet_content': py_style_sheet_content,
            'zoom': settings.DEFAULT_ZOOM,
            'center':[settings.DEFAULT_LAT, settings.DEFAULT_LON],
        }
    )

def save(request, name):
    style_sheet_to_save = join(py_style_sheets_dir, name + '.py')
    with open(style_sheet_to_save, 'w') as fd:
        fd.write(request.body)
    return HttpResponse('Style sheet successfully saved')

def preview(request, name):
    tmp_dir = tempfile.gettempdir()
    py_style_sheet_path = join(tmp_dir, name + '.py')
    with open(py_style_sheet_path, 'w') as f:
       f.write(request.body)
    py_style_sheet = pycnik.import_style(py_style_sheet_path)
    pycnik.translate(py_style_sheet, join(tmp_dir, name + '.xml'))
    return HttpResponse('Style sheet successfully applied')

