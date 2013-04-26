"""
    WebVirt URL Handlers
"""
import config

class Index:
    def GET(self):
        return "<h1>%s</h1>" %(config.name)

classes = globals()
