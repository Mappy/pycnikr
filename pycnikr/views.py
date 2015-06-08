# -*- coding: utf-8 -*-

from os import listdir
from os.path import dirname, join, split, splitext
import tempfile

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

from pycnik import pycnik

def get_py_style_sheet_path(name):
    return settings.PYCNIKR_STYLE_SHEETS_MAPPING[name][0]

def get_xml_style_sheet_path(name):
    return settings.PYCNIKR_STYLE_SHEETS_MAPPING[name][1]

def get_py_style_sheets():
    return settings.PYCNIKR_STYLE_SHEETS_MAPPING.keys()

@require_GET
@ensure_csrf_cookie
def template(request, name):
    py_style_sheets = filter(lambda x: x != name, get_py_style_sheets())
    with open(get_py_style_sheet_path(name), 'r') as fd:
        py_style_sheet_content = fd.read()
    return render(
        request, 'pycnikr/template.html',
        {
            'tile_server_url': settings.PYCNIKR_TILE_SERVER_URL,
            'style_sheets': py_style_sheets,
            'name': name,
            'style_sheet_content': py_style_sheet_content,
            'zoom': settings.PYCNIKR_DEFAULT_ZOOM,
            'center':[settings.PYCNIKR_DEFAULT_CENTER_LAT,
                      settings.PYCNIKR_DEFAULT_CENTER_LON],
            }
        )
@require_POST
def save(request, name):
    with open(get_py_style_sheet_path(name), 'w') as fd:
        fd.write(request.body)
    return HttpResponse('Style sheet successfully saved')

@require_POST
def preview(request, name):
    xml_style_sheet_path = get_xml_style_sheet_path(name)
    py_style_sheet_path = splitext(xml_style_sheet_path)[0] + '.py'
    with open(py_style_sheet_path, 'w') as fd:
       fd.write(request.body)
    py_style_sheet = pycnik.import_style(py_style_sheet_path)
    pycnik.translate(py_style_sheet, get_xml_style_sheet_path(name))
    return HttpResponse('Style sheet successfully applied')

@require_GET
def home(request):
    return render(
        request, 'pycnikr/index.html',
        {
            'style_sheets': get_py_style_sheets(),
        }
    )

