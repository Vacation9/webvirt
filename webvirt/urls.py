"""
    WebVirt URL Handlers
"""
import auth
import config
from conn import conn

import web

class Index:
    def GET(self):
        templates = web.template.render('webvirt/templates/')
	content = "This is some random text for testing."
        return templates.index(content)

class Auth:
    def GET(self):
        web.header('Content-type', 'text/html')
        return "<h1>Incorrect method</h1>"

    def POST(self):
        data = web.data()
        return str(data)

class Login:
    def GET(self):
        templates = web.template.render('webvirt/templates/')
        return templates.login()

class List:
    def GET(self):
        return conn.listDefinedDomains()



classes = globals()
