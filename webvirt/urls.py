"""
    WebVirt URL Handlers
"""
import ajax
import auth
import common
import config
import libvirt
from connection import conn
import virt
import web

class Index:
    def GET(self):
        auth.verify_auth("http://www.tjhsst.edu/hackathon/login")
        templates = web.template.render('webvirt/templates/')
        content = "This is some random text for testing."
        data = ""
        for dom in conn.listAllDomains(0):
            dom = virt.Domain(dom)
            if(dom.rawstate == libvirt.VIR_DOMAIN_RUNNING):
                data += "<li><a href='/hackathon/vm?vm=" + dom.name + "'>" + dom.name + "<div class='pull-right'i style='color:#00FF00'>" + dom.state + "</div></a></li>"
            elif(dom.rawstate == libvirt.VIR_DOMAIN_SHUTOFF):
                data += "<li><a href='/hackathon/vm?vm=" + dom.name + "'>" + dom.name + "<div class='pull-right'i style='color:#FF0000'>" + dom.state + "</div></a></li>"
            else:
                data += "<li><a href='/hackathon/vm?vm=" + dom.name + "'>" + dom.name + "<div class='pull-right'i style='color:#FF9900'>" + dom.state + "</div></a></li>"
        return templates.index(content, data)

class Host:
    def GET(self): 
        auth.verify_auth("http://www.tjhsst.edu/hackathon/login")
        templates = web.template.render('webvirt/templates/')
        host = Host()
        content = ""
        data = ""
	hs = virt.HostServer()
	content += "Hostname: " + hs.hostname + "<br />"
	content += "Host type: " + hs.hosttype + "<br />"
	#content += "Host capabilities: " + hs.caps + "\n"
	#content += "Host CPU Statistics: " + str(hs.cpustats) + "\n"
	#content += "Host CPU Map: " + str(hs.cpumap) + "\n"
	content += "Host Memory Statistics: " + str(hs.memstats) + "<br />"
	#content += "Other Host Information: " + str(hs.info) + "\n"
        for dom in conn.listAllDomains(0):
            dom = virt.Domain(dom)
            if(dom.rawstate == libvirt.VIR_DOMAIN_RUNNING):
                data += "<li><a href='/hackathon/vm?vm="+ dom.name + "'>" + dom.name + "<div class='pull-right'i style='color:#00FF00'>" + dom.state + "</div></a></li>"
            elif(dom.rawstate == libvirt.VIR_DOMAIN_SHUTOFF):
                data += "<li><a href='/hackathon/vm?vm="+ dom.name + "'>" + dom.name + "<div class='pull-right'i style='color:#FF0000'>" + dom.state + "</div></a></li>"
            else:
                data += "<li><a href='/hackathon/vm?vm="+ dom.name + "'>" + dom.name + "<div class='pull-right'i style='color:#FF9900'>" + dom.state + "</div></a></li>"
        return templates.index(content, data)


class VM:
    def GET(self):
        cookies = web.cookies()
        if cookies.get("session") == None:
            web.seeother("http://www.tjhsst.edu/hackathon/login")
        templates = web.template.render('webvirt/templates/')
        data2 = web.input()
	content = ""
        vm = data2['vm']
	domObj = virt.Domain(conn.lookupByName(vm))
	if 'action' in data2.keys():
	    if data2[action] == 'start':
	        domObj.startVM()
	    elif data2[action] == 'stop':
	        domObj.stopVM()
	    elif data2[action] == 'destroy':
	        domObj.destroyVM()
	    elif data2[action] == 'suspend':
	        domObj.suspendVM()
	    elif data2[action] == 'resume':
	        domObj.resumeVM()
	    if data2[action] in ['start', 'stop', 'destroy', 'suspend', 'resume']:
	        content += '<h3>' + vm + ' ' +  action + ('p' if data[2] == 'stop' else '') + 'ed.</h3>'
        content += "<input type=button onClick='location.href='/hackathon/vm?vm=" + vm + "&action=start' value='Start'>\
        <br><input type=button onClick='location.href='/hackathon/vm?vm=" + vm + "'&action=stop' value='Stop'>\
        <br><input type=button onClick='location.href='/hackathon/vm?vm=" + vm + "'&action=destroy' value='Destroy'>\
        <br><input type=button onClick='location.href='/hackathon/vm?vm=" + vm + "'&action=suspend' value='Suspend'>\
        <br><input type=button onClick='location.href='/hackathon/vm?vm=" + vm + "'&action=resume' value='Resume'>"
        data = ""
        for dom in conn.listAllDomains(0):
            dom = virt.Domain(dom)
            if(dom.rawstate == libvirt.VIR_DOMAIN_RUNNING):
                data += "<li><a href='/hackathon/vm?vm=" + dom.name + "'>" + dom.name + "<div class='pull-right'i style='color:#00FF00'>" + dom.state + "</div></a></li>"
            elif(dom.rawstate == libvirt.VIR_DOMAIN_SHUTOFF):
                data += "<li><a href='/hackathon/vm?vm=" + dom.name + "'>" + dom.name + "<div class='pull-right'i style='color:#FF0000'>" + dom.state + "</div></a></li>"
            else:
                data += "<li><a href='/hackathon/vm?vm=" + dom.name + "'>" + dom.name + "<div class='pull-right'i style='color:#FF9900'>" + dom.state + "</div></a></li>"
        return templates.vm(content, data, vm)

class Create:
    def GET(self):
        cookies = web.cookies()
        if cookies.get("session") == None:
            web.seeother("http://www.tjhsst.edu/hackathon/login")
        templates = web.template.render('webvirt/templates/')
        content = ""
        data = ""
        for dom in conn.listAllDomains(0):
            dom = virt.Domain(dom)
            if(dom.rawstate == libvirt.VIR_DOMAIN_RUNNING):
                data += "<li><a href='/hackathon/vm?vm=" + dom.name + "'>" + dom.name + "<div class='pull-right'i style='color:#00FF00'>" + dom.state + "</div></a></li>"
            elif(dom.rawstate == libvirt.VIR_DOMAIN_SHUTOFF):
                data += "<li><a href='/hackathon/vm?vm=" + dom.name + "'>" + dom.name + "<div class='pull-right'i style='color:#FF0000'>" + dom.state + "</div></a></li>"
            else:
                data += "<li><a href='/hackathon/vm?vm=" + dom.name + "'>" + dom.name + "<div class='pull-right'i style='color:#FF9900'>" + dom.state + "</div></a></li>"
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
        auth.verify_auth("http://www.tjhsst.edu/hackathon/login")
        data = []
        for dom in conn.listAllDomains(0):
            data[dom] = Domain(dom)
        return web.template.render('webvirt/templates/').index(data)

class Console:
    def GET(self):
        auth.verify_auth("http://www.tjhsst.edu/hackathon/login")
        templates = web.template.render('webvirt/templates/')
        return templates.console()

class Ajax:
    def GET(self, path=''):
        authed = auth.verify_auth()
        if not authed:
            web.ctx.status = '401 Unauthorized'
            return "{}"
        components = path.split('/')
        ajax_handler = ajax.AjaxHandler()
        ajax_handler.add_handler('vminfo', ajax.vminfo)
        ret = ajax_handler.handle(components)
        if ret:
            return ret
        web.ctx.status = '404 Not Found'
        return '{}'

classes = globals()
