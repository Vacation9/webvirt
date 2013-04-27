"""
    WebVirt URL Handlers
"""
import auth
import config
from conn import conn

import web

class Index:
    def GET(self):
        templates = web.template.render('webvirt/templates/, base='index'')
        return templates.index()

class Auth:
    def GET(self):
        web.header('Content-type', 'text/html')
        return "<h1>Incorrect method</h1>"

    def POST(self):
        data = web.data()
        return "Hello" + str(data)

class Login:
    def GET(self):
        templates = web.template.render('webvirt/templates/')
        return templates.login()

class List:
    def GET(self):
        return conn.listDefinedDomains()



classes = globals()
