import libvirt
from connection import conn
import common

class Domain:
    def __init__(self, dom):
        self.dom = dom
        self.name = dom.name()
        self.rawstate = dom.state(0)[0]
        self.state = common.getState(self.rawstate)
    def startVM(self):
        self.dom.create()
    def stopVM(self):
        self.dom.shutdown()
    def destroyVM(self):
        self.dom.destroy()
    def suspendVM(self):
        self.dom.suspend()
    def resumeVM(self):
        self.dom.resume()

    def get_dict(self):
        return {
                "name": self.name,
                "state": self.state
                }

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

        def createDomain(self,name,mem,cpu,hd,iso,pts):
                dom = conn.defineXML("""
               <domain type="kvm">
                   <name>%s</name>
                   <memory>%d</memory>
                   <vcpu>%d</vcpu>
                   <os>
                        <type arch="x86_64">hvm</type>
                        <boot dev="cdrom"/>
                   </os>
                   <devices>
                       <disk type="block" device="disk">
                            <source dev="%s"/>
                            <target dev="hda" bus="virtio"/>
                       </disk>
                       <disk type='file' device='cdrom'>
                            <!--<driver name='qemu' type='raw'/>-->
                            <source file='%s'/>
                            <target dev='hdc' bus='ide' tray='closed'/>
                            <readonly/>
                       </disk>
                       <interface type="bridge">
                           <source bridge="vbr1600"/>
                           <model type="virtio"/>
                       </interface>
                       <graphics type="vnc" port="-1" autoport="yes"/>
                       <console type='pty'>
                           <source path='/dev/pts/%d' />
                           <target type='serial' port='0' />
                       </console>
                    </devices>
                </domain>
                """ % (name,mem,cpu,hd,iso,pts)
        )
                self.domains.append(dom)
                return dom


