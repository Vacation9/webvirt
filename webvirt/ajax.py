from connection import conn
import json
import virt
import web

class AjaxHandler:
    def __init__(self):
        self.handlers = {}

    def handle(self, path):
        if len(path) < 1:
            return
        root = path[0]
        if root in self.handlers:
            return self.handlers[root](root, path[1:])
        return False

    def add_handler(self, func, path):
        if path not in self.handlers:
            self.handlers[path] = func

def vminfo(path, params):
    hs = virt.HostServer()
    if len(params) < 1:
        web.ctx.status = "400 Bad Request"
        return "{}"
    vm = params.pop(0)
    for dom in hs.domains:
        if dom.name == vm:
            info = dom.get_dict()
            if len(params) > 0:
                field = params.pop(0)
                if field in info:
                    return json.dumps({field: info[field]})
                web.ctx.status = "404 Not Found"
                return "{}"
            return json.dumps(info)
    web.ctx.status = "404 Not Found"
    return "{}"

def listvms(path, params):
    hs = virt.HostServer()
    vlist = []
    for dom in hs.domains:
        vlist.append(dom.name)
    return json.dumps({'vms': vlist})
