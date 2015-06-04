# -*- coding: utf-8 -*-

from os import listdir
from os.path import dirname, join, split, splitext
import tempfile

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from pycnik import pycnik

def get_py_style_sheets():
    return filter(lambda file_name: file_name.endswith('.py'),
                  listdir(settings.PYCNIKR_STYLE_SHEETS_DIR))

def get_normalized_name(name):
    return name if name.endswith('.py') else name + '.py'

def get_raw_name(name):
    return splitext(name)[0]

@ensure_csrf_cookie
def template(request, name):
    name = get_normalized_name(name)
    py_style_sheets = filter(lambda x: x != name, get_py_style_sheets())
    py_style_sheet = open(join(settings.PYCNIKR_STYLE_SHEETS_DIR, name), 'r')
    py_style_sheet_content = py_style_sheet.read()
    return render(
        request, 'pycnikr/index.html',
        {
            'style_sheets': py_style_sheets,
            'name': name,
            'raw_name': get_raw_name(name),
            'style_sheet_content': py_style_sheet_content,
            'zoom': settings.PYCNIKR_DEFAULT_ZOOM,
            'center':[settings.PYCNIKR_DEFAULT_CENTER_LAT,
                      settings.PYCNIKR_DEFAULT_CENTER_LON],
        }
    )

def save(request, name):
    name = get_normalized_name(name)
    py_style_sheets_dir = settings.PYCNIKR_STYLE_SHEETS_DIR
    style_sheet_to_save = join(py_style_sheets_dir, name)
    with open(style_sheet_to_save, 'w') as fd:
        fd.write(request.body)
    return HttpResponse('Style sheet successfully saved')

def preview(request, name):
    name = get_normalized_name(name)
    tmp_dir = settings.PYCNIKR_TMP_STYLE_SHEETS_DIR
    py_style_sheet_path = join(tmp_dir, name)
    with open(py_style_sheet_path, 'w') as f:
       f.write(request.body)
    py_style_sheet = pycnik.import_style(py_style_sheet_path)
    raw_name = get_raw_name(name)
    pycnik.translate(py_style_sheet, join(tmp_dir, raw_name + '.xml'))
    return HttpResponse('Style sheet successfully applied')

def home(request):
    return render(
        request, 'pycnikr/home.html',
        {
            'style_sheets': get_py_style_sheets(),
        }
    )

