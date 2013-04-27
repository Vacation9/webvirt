from connection import conn
import common

class Domain:
    def __init__(self, dom):
        self.dom = dom
        self.name = self.dom.name()
        self.rawstate = self.dom.state(0)[0]
        self.state = common.getState(self.rawstate)

class Host:
    def __init__(self):
        self.hostname = conn.getHostname()
        self.type = conn.getType()
        self.caps = conn.getCapabilites()
        self.cpustats = conn.getCPUStats(libvirt.VIR_NODE_CPU_STATS_ALL_CPUS,0)
        self.cpumap = conn.getCPUMap(0)
        self.info = conn.getInfo()
        self.memstats = conn.getMemoryStats(libvirt.VIR_NODE_MEMORY_STATS_ALL_CELLS,0)
    def createDomain(self):
        return 'bob'
