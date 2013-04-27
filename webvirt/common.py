"""
    Common functions
"""

import libvirt

def parse_post(data):
    ret = {}
    fields = data.split('&')
    for item in fields:
        if '=' in item:
            key, value = item.split('=')
            ret[key] = value
    return ret

def getState(state):
    if state == libvirt.VIR_DOMAIN_NOSTATE:
        return "No State."
    elif state == libvirt.VIR_DOMAIN_RUNNING:
        return "Running."
    elif state == libvirt.VIR_DOMAIN_BLOCKED:
        return "Blocked on a resource."
    elif state == libvirt.VIR_DOMAIN_PAUSED:
        return "Paused."
    elif state == libvirt.VIR_DOMAIN_SHUTDOWN:
        return "Shutting down."
    elif state == libvirt.VIR_DOMAIN_SHUTOFF:
        return "Shut off."
    elif state == libvirt.VIR_DOMAIN_CRASHED:
        return "Crashed."
    elif state == libvirt.VIR_DOMAIN_PMSUSPENDED:
        return "Suspended."
    else:
        raise Exception("This should never happen. state=" + state)

def allinfo(doms):
    ret = {}
    for dom in doms:
        ret[dom.name] = (dom.get_dict())
    return ret

def pct_from_mem(memstats):
    free = memstats['free'] / memstats['total']
    import sys
    sys.stderr.write(str(free) + '\n')
    free = round(free * 100)
    used = 100 - free
    return (free, used)
