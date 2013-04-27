"""
    WebVirt URL Handlers
"""
import auth
import common
import config
import libvirt
from connection import conn
from virt import Domain

import web

class Index:
    def GET(self):
        cookies = web.cookies()
        if cookies.get("session") == None:
            web.seeother("http://www.tjhsst.edu/hackathon/login")
        templates = web.template.render('webvirt/templates/')
        content = "This is some random text for testing."
        data = ""
        domains = conn.listDefinedDomains()
        for dom in domains:
                dom = conn.lookupByName(dom)
                data += "<li><a href='#'>" + dom.name() + common.getState(dom.state(0)[0]) + "</a></li>"
        return templates.index(content, data)

class Auth:
    def GET(self):
        web.header('Content-type', 'text/html')
        return "<h1>Incorrect method</h1>"

    def POST(self):
        data = web.input()
        try:
            username = data['username']
            password = data['password']
            if auth.authuser(username, password):
                if 'redirect' in data:
                    web.seeother(data['redirect'])
                else:
                    web.seeother("http://www.tjhsst.edu/hackathon/")
            else:
                web.seeother("http://www.tjhsst.edu/hackathon/login?failed=1")
        except Exception as e:
            return "Caught " + str(e) + " on login auth"

class Login:
    def GET(self):
        templates = web.template.render('webvirt/templates/')
        data = web.input()
        if "failed" in data:
            return templates.login('<span><p style="color:#FF0000">Failed Login</p></span>')
        else:
            return templates.login('')

class List:
    def GET(self):
        data = []
        for dom in conn.listDefinedDomains():
            data[dom] = Domain(dom)
        return web.template.render('webvirt/templates/').index(data)

class Console:
    def GET(self):
        templates = web.template.render('webvirt/templates/')
	domObj = conn.lookupByName(web.input()['domain'])
	streamObj = libvirt.virStream(conn)
	streamObjStatus = domObj.openConsole(streamObj)
	if streamObj == 0:
	    return streamObj
	elif streamObj == -1:
	    return 'Error opening stream object'
	else:
	    return 'Something very, very bad happened'

classes = globals()
