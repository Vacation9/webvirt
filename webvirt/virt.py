from connection import conn
import common

class Domain:
    def __init__(self, dom):
        self.dom = dom
        self.name = self.dom.name()
        self.state = common.getState(self.dom.state(0)[0])

