"""
    WebVirt URL Handlers
"""
import auth
import common
import config
import libvirt
from connection import conn
from virt import Domain,Host
import web

class Index:
    def GET(self):
        cookies = web.cookies()
        if cookies.get("session") == None:
            web.seeother("http://www.tjhsst.edu/hackathon/login")
        templates = web.template.render('webvirt/templates/')
        content = "This is some random text for testing."
        data = ""
        for dom in conn.listAllDomains(0):
            dom = Domain(dom)
            if(dom.rawstate == libvirt.VIR_DOMAIN_RUNNING):
                data += "<li><a href='#'>" + dom.name + "<div class='pull-right'i style='color:#00FF00'>" + dom.state + "</div></a></li>"
            elif(dom.rawstate == libvirt.VIR_DOMAIN_SHUTOFF):
                data += "<li><a href='#'>" + dom.name + "<div class='pull-right'i style='color:#FF0000'>" + dom.state + "</div></a></li>"
            else:
                data += "<li><a href='#'>" + dom.name + "<div class='pull-right'i style='color:#FF9900'>" + dom.state + "</div></a></li>"
        return templates.index(content, data)

class Host:
    def GET(self):
        cookies = web.cookies()
        if cookies.get("session") == None:
            web.seeother("http://www.tjhsst.edu/hackathon/login")
        templates = web.template.render('webvirt/templates/')
        host = Host()
        content = ""
        data = ""
        for dom in conn.listAllDomains(0):
            dom = Domain(dom)
            if(dom.rawstate == libvirt.VIR_DOMAIN_RUNNING):
                data += "<li><a href='#'>" + dom.name + "<div class='pull-right'i style='color:#00FF00'>" + dom.state + "</div></a></li>"
            elif(dom.rawstate == libvirt.VIR_DOMAIN_SHUTOFF):
                data += "<li><a href='#'>" + dom.name + "<div class='pull-right'i style='color:#FF0000'>" + dom.state + "</div></a></li>"
            else:
                data += "<li><a href='#'>" + dom.name + "<div class='pull-right'i style='color:#FF9900'>" + dom.state + "</div></a></li>"
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
        streamObjStatus = domObj.openConsole(None, streamObj, 0)
        if streamObjStatus == 0:
            return streamObj
        elif streamObjStatus == -1:
            return 'Error opening stream object'
        else:
            return 'Something very, very bad happened'

classes = globals()
