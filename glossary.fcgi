#!/home1/gregoso6/public_html/slate/venv/bin/python

from flup.server.fcgi import WSGIServer
from slate import app as application

WSGIServer(application).run()
