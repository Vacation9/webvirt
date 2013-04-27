"""
    WebVirt URL Handlers
"""
import config

import web

class Index:
    def GET(self):
        templates = web.template.render('templates/')
        return templates.index()

class Auth:
    def GET(self):
        web.header('Content-type', 'text/html')
        return "<h1>Incorrect method</h1>"

    def POST(self):
        data = web.data()
        return str(data)

classes = globals()
