from os.path import join, dirname

from django.shortcuts import render

stylesheets_dir = join(dirname(__file__), 'stylesheets')

def template(request, name):
    name=name if name.endswith('.py') else name+'.py'
    stylesheet = open(join(stylesheets_dir, name), 'r')
    content = stylesheet.read()

    return render(
        request, 'main_app/hello.html',
        {
            "name": "pycnikr",
            'stylesheet_content': content,
        }
    )
