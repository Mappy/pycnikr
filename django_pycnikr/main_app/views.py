from os.path import join, dirname

from django.shortcuts import render
from django.http import HttpResponse
import pycnik

stylesheets_dir = join(dirname(__file__), 'stylesheets')

def template(request, name):
    name = name if name.endswith('.py') else name + '.py'
    stylesheet = open(join(stylesheets_dir, name), 'r')
    content = stylesheet.read()

    return render(
        request, 'main_app/hello.html',
        {
            "name": name[:-3],
            'stylesheet_content': content,
        }
    )

def pycnik(request, stylesheet):
    print stylesheet
    print request.POST
    return HttpResponse('Stylesheet successfully applied')
