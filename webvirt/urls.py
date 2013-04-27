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
        data = web.input()
        try:
            username = data['username']
            password = data['password']
            auth.authuser(username, password)
        except Exception as e:
            return "Caught " + str(e) + " on login auth"

class Login:
    def GET(self):
        templates = web.template.render('webvirt/templates/')
        data = web.input()
        return str(data)
        #data = common.parse_post(data)
        #if "failed" in data:
        #    return templates.login('<h3><p style="background-color:#FF0000">Failed Login</p></h3>')
        #else:
        #    return templates.login('')

class List:
    def GET(self):
        data = ""
        domains = conn.listDefinedDomains()
        for dom in domains:
            dom = conn.lookupByName(dom)
            data += "name=" + dom.name() + "\n"
            data += dom.state()
            #data += "state=" + common.getState(dom.state()[0]) + "\n"
        return data

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
