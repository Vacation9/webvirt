import libvirt
from connection import conn
import common

class Domain:
    def __init__(self, dom):
        self.dom = dom
        self.name = dom.name()
        self.rawstate = dom.state(0)[0]
        self.state = common.getState(self.rawstate)

class HostServer:
    def __init__(self):
        self.hostname = conn.getHostname()
        self.hosttype = conn.getType()
        self.caps = conn.getCapabilities()
        self.cpustats = conn.getCPUStats(libvirt.VIR_NODE_CPU_STATS_ALL_CPUS,0)
        self.cpumap = conn.getCPUMap(0)
        self.info = conn.getInfo()
        self.memstats = conn.getMemoryStats(libvirt.VIR_NODE_MEMORY_STATS_ALL_CELLS,0)
        self.domains = [Domain(dom) for dom in conn.listAllDomains(0)]

    def createDomain(self,name):
        dom = conn.defineXML(
                """<domain type='kvm'>
                <name>%s</name>
                <memory>512</memory>
                <os>
                <type>hvm</type>
                </os>
                </domain>""" % (name)
                )
        self.domains.append(dom)
        return dom
