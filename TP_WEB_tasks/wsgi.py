"""
WSGI config for TP_WEB_tasks project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from pprint import pformat
from urllib.parse import parse_qs

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TP_WEB_tasks.settings')

application = get_wsgi_application()


def app(environ, start_response):
    output = [b'<p>Hello world!</p>', ]

    # create a simple POST form:
    output.append(b'<form method="POST">')
    output.append(b'<input type="text" name="test">')
    output.append(b'<input type="submit">')
    output.append(b'</form>')

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    request_body = environ['wsgi.input'].read(request_body_size)

    if environ['REQUEST_METHOD'] == 'POST':
        output.append(b'<h3>POST DATA</h3>')
        output.append(request_body)

    if environ['REQUEST_METHOD'] == 'GET':
        d = parse_qs(environ['QUERY_STRING'])
        if d != {}:
            output.append(b'<h3>GET DATA:</h3>')
            for key, value in d.items():
                output.append((str(key) + ' = ' + str(value)).encode())
                output.append(b'<br>')

    # send results
    output_len = sum(len(line) for line in output)
    start_response('200 OK', [('Content-type', 'text/html'),
                              ('Content-Length', str(output_len))])

    return output
