#!/home3/gregoso6/public_html/gloss/venv/bin/python

from flup.server.fcgi import WSGIServer
from gloss import app as application

WSGIServer(application).run()
