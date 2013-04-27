"""
    WebVirt URL Handlers
"""
import config
from conn import conn

import web

class Index:
    def GET(self):
        templates = web.template.render('webvirt/templates/')
        return templates.index()

class Auth:
    def GET(self):
        web.header('Content-type', 'text/html')
        return "<h1>Incorrect method</h1>"

    def POST(self):
        data = web.data()
        return str(data)
class List:
    def GET(self):
        return conn.listDefinedDomains()


classes = globals()
