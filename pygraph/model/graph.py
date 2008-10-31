
class SubscribableModel(object):
    def __init__(self):
        self._evhs = []
        self._children = []
    def subscribe(self, evh):
        self._evhs.append(evh)
    def unsubscribe(self, evh):
        self._evhs.remove(evh)
    def post(self, name, *args):
        for evh in self._evhs:
            if hasattr(evh,name):
                getattr(evh,name)(*args)
    def setProperty(self, name, value):
        setattr(self,name,value)
        self.post("propertychange",name,value)
    def getProperty(self, name):
        return getattr(self,name)
    def addChild(self, child):
        self._children.append(child)
        self.post("addchild",child)
    def delChild(self, child):
        self._children.remove(child)
        self.post("delchild",child)

class GraphModel(SubscribableModel):
    def __init__(self):
        SubscribableModel.__init__(self)

class GraphNodeModel(SubscribableModel):
    def __init__(self):
        SubscribableModel.__init__(self)

class GraphNodeConnectorModel(SubscribableModel):
    def __init__(self):
        SubscribableModel.__init__(self)

class GraphConnectionModel(SubscribableModel):
    def __init__(self,origin=None,destination=None):
        SubscribableModel.__init__(self)
        self.origin = origin
        self.destination = destination

if __name__ == "__main__":
    print "run test"
    graphmodel = GraphModel()
    newnode = GraphNodeModel()
    # subscribe
    class myevh(object):
        def propertychange(self,name,value):
            print " * propertychanged!",name,value
        def addchild(self,child):
            print " * addchild",child
        def delchild(self,child):
            print " * delchild",child
    graphmodel.subscribe(myevh())
    newnode.subscribe(myevh())
    # change property
    newnode.setProperty("name","bla")
    # add/remove node to graph
    graphmodel.addChild(newnode)
    graphmodel.delChild(newnode)
    graphmodel.addChild(newnode)
    # add/remove connectors to graph
    newconnector = GraphNodeConnectorModel()
    newconnector.subscribe(myevh())
    newconnector.setProperty("name","bla")
    assert newconnector.getProperty("name") == "bla"
    assert newconnector.name == "bla"
    newnode.addChild(newconnector)
    newnode.delChild(newconnector)
    newnode.addChild(newconnector)
    # create connections
    newnode2 = GraphNodeModel()
    newconnector2 = GraphNodeConnectorModel()
    newnode2.addChild(newconnector2)
    newconnection = GraphConnectionModel(newconnector,newconnector2)
    graphmodel.addChild(newconnection)
    graphmodel.delChild(newconnection)
    graphmodel.addChild(newconnection)

