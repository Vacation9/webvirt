"""
    WebVirt URL Handlers
"""
import auth
import common
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
        data = common.parsepost(data)
        try:
            username = data['username']
            password = data['password']
            auth.authuser(username, password)

class Login:
    def GET(self,failed):
        templates = web.template.render('webvirt/templates/')
        if(failed = 1):
		return templates.login('<h3><p style="background-color:#FF0000">Failed Login</p></h3>')
	else:
		return templates.login()


class List:
    def GET(self):
        return conn.listDefinedDomains()

class Console:
    def GET(self, domain):
        templates = web.template.render('webvirt/templates/')
	domObj = conn.lookupByName(domain)
	streamObj = None
	streamObjStatus = domObj.openConsole(streamObj)
	if streamObj == 0:
	    return streamObj
	elif streamObj == -1:
	    return 'Error opening stream object'
	else:
	    return 'Something very, very bad happened'

classes = globals()
