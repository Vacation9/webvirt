"""
    WebVirt URL Handlers
"""
import config

import web

class Index:
    def GET(self):
        web.header('Content-type', 'text/html')
        return "<h1>%s</h1>" %(config.name)

class Auth:
    def POST(self):
        data = web.data()
        return str(data)

classes = globals()
