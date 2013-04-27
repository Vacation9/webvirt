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
        content = ""
        numVMs = float(len(conn.listAllDomains(0)))
        perRunningVMs = 100 * (float(len(conn.listAllDomains(16)))) / numVMs
        perSuspendVMs = 100 * (float(len(conn.listAllDomains(32)))) / numVMs
        perShutoffVMs = 100 * (float(len(conn.listAllDomains(64)))) / numVMs
        content += '<h2>VM State Statistics</h2><br />\n'
        content += '<div class="progress">\n'
        content += '  <div class="bar bar-success" style="width: ' + str(perRunningVMs) + '%;">Running</div>\n'
        content += '  <div class="bar bar-warning" style="width: ' + str(perSuspendVMs) + '%;">Suspended</div>\n'
        content += '  <div class="bar bar-danger" style="width: ' + str(perShutoffVMs) + '%;">Shut Down</div>\n'
        content += '</div>\n'
        data = ""
        hs = virt.HostServer()
        freemem, usedmem = common.pct_from_mem(hs.memstats)
        usedmem = str(usedmem) + '%'
        content += str(templates.host(hs.hostname, hs.hosttype, usedmem))
        for dom in conn.listAllDomains(0):
            dom = virt.Domain(dom)
            if(dom.rawstate == libvirt.VIR_DOMAIN_RUNNING):
                data += "<li><a href='/hackathon/vm?vm=" + dom.name + "'>" + dom.name + "<div class='pull-right'><span class='label label-success'>" + dom.state + "</span></div></a></li>"
            elif(dom.rawstate == libvirt.VIR_DOMAIN_SHUTOFF):
                data += "<li><a href='/hackathon/vm?vm=" + dom.name + "'>" + dom.name + "<div class='pull-right'><span class='label label-important'>" + dom.state + "</span></div></a></li>"
            else:
                data += "<li><a href='/hackathon/vm?vm=" + dom.name + "'>" + dom.name + "<div class='pull-right'><span class='label label-warning'>" + dom.state + "</span></div></a></li>"
        return templates.index(content, data)

class Host:
    def GET(self): 
        auth.verify_auth("http://www.tjhsst.edu/hackathon/login")
        templates = web.template.render('webvirt/templates/')
        host = Host()
        data = ""
        hs = virt.HostServer()
        freemem, usedmem = common.pct_from_mem(hs.memstats)
        freemem, usedmed = [str(x) + '%' for x in (freemem, usedmem)]
        content = templates.host(hs.hostname, hs.hosttype, freemem, usedmem)
        for dom in conn.listAllDomains(0):
            dom = virt.Domain(dom)
            if(dom.rawstate == libvirt.VIR_DOMAIN_RUNNING):
                data += "<li><a href='/hackathon/vm?vm="+ dom.name + "'>" + dom.name + "<div class='pull-right'><span class='label label-success'>" + dom.state + "</span></div></a></li>"
            elif(dom.rawstate == libvirt.VIR_DOMAIN_SHUTOFF):
                data += "<li><a href='/hackathon/vm?vm="+ dom.name + "'>" + dom.name + "<div class='pull-right'><span class='label label-important'>" + dom.state + "</span></div></a></li>"
            else:
                data += "<li><a href='/hackathon/vm?vm="+ dom.name + "'>" + dom.name + "<div class='pull-right'><span class='label label-warning'>" + dom.state + "</span></div></a></li>"
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
            if data2['action'] == 'start':
                domObj.startVM()
            elif data2['action'] == 'stop':
                domObj.stopVM()
            elif data2['action'] == 'destroy':
                domObj.destroyVM()
            elif data2['action'] == 'suspend':
                domObj.suspendVM()
            elif data2['action'] == 'resume':
                domObj.resumeVM()
            if data2['action'] in ['start', 'stop', 'destroy', 'suspend', 'resume']:
	        content += '<div class="alert">\n'
		content += '  <button type="button" class="close" data-dismiss="alert">&times;</button>'
                content += '  ' + vm + ' ' +  data2['action'] + ('p' if data2['action'] == 'stop' else '') + ('e' if data2['action'] != 'resume' else '') + 'd.'
		content += '</div>'
        content += "<div class=\"btn-group\">\n<a class=\"btn dropdown-toggle\" data-toggle=\"dropdown\" href=\"#\">Power Options<span class=\"caret\"></span></a>\n<ul class=\"dropdown-menu\"><li><a href=\"/hackathon/vm?vm=" + vm + "&action=start\">Start</a></li>\n<li><a href=\"/hackathon/vm?vm=" + vm + "&action=stop\">Stop</a></li>\n<li><a href=\"/hackathon/vm?vm=" + vm + "&action=destroy\">Destroy</a></li>\n<li><a href=\"/hackathon/vm?vm=" + vm + "&action=suspend\">Suspend</a></li>\n<li><a href=\"/hackathon/vm?vm=" + vm + "&action=resume\">Resume</a></li></ul></div>"
        data = ""
        for dom in conn.listAllDomains(0):
            dom = virt.Domain(dom)
            if(dom.rawstate == libvirt.VIR_DOMAIN_RUNNING):
                data += "<li><a href='/hackathon/vm?vm=" + dom.name + "'>" + dom.name + "<div class='pull-right'><span class='label label-success'>" + dom.state + "</span></div></a></li>"
            elif(dom.rawstate == libvirt.VIR_DOMAIN_SHUTOFF):
                data += "<li><a href='/hackathon/vm?vm=" + dom.name + "'>" + dom.name + "<div class='pull-right'><span class='label label-important'>" + dom.state + "</span></div></a></li>"
            else:
                data += "<li><a href='/hackathon/vm?vm=" + dom.name + "'>" + dom.name + "<div class='pull-right'><span class='label label-warning'>" + dom.state + "</span></div></a></li>"
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
                data += "<li><a href='/hackathon/vm?vm=" + dom.name + "'>" + dom.name + "<div class='pull-right'><span class='label label-success'>" + dom.state + "</span></div></a></li>"
            elif(dom.rawstate == libvirt.VIR_DOMAIN_SHUTOFF):
                data += "<li><a href='/hackathon/vm?vm=" + dom.name + "'>" + dom.name + "<div class='pull-right'><span class='label label-important'>" + dom.state + "</span></div></a></li>"
            else:
                data += "<li><a href='/hackathon/vm?vm=" + dom.name + "'>" + dom.name + "<div class='pull-right'><span class='label label-warning'>" + dom.state + "</span></div></a></li>"
        return templates.create(content, data,form)

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

classes = globals()
