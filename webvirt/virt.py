from connection import conn
import common

class Domain:
    def __init__(self, id):
        self.dom = conn.lookupByID(id)
        self.name = self.dom.name()
        self.state = common.getState(self.dom.state(0)[0])

