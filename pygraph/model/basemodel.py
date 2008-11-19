import uuid
from meta import SubscribableModelMeta,ClassRegistry

########################################################
# reference model
class SubscribableModel(object):
    __metaclass__ = SubscribableModelMeta
    def __init__(self,instance_uuid=None):
        self._evhs = []
        self._children = []
        self._props = {}
        if instance_uuid:
            self.uuid = uuid.UUID(instance_uuid)
        else:
            self.uuid = uuid.uuid1()
    def new(self, clsname,*args):
        return ClassRegistry[clsname](*args)
    def subscribe(self, evh):
        self._evhs.append(evh)
    def unsubscribe(self, evh):
        self._evhs.remove(evh)
    def post(self, name, *args):
        for evh in self._evhs:
            if hasattr(evh,name):
                getattr(evh,name)(*args)
    def setProperty(self, name, value):
        self._props[name] = value
        self.post("propertychange",name,value)
    def getProperty(self, name):
        return self._props[name]
    def getProperties(self):
        return self._props.keys()
    def addChild(self, child):
        self._children.append(child)
        self.post("addchild",child)
    def delChild(self, child):
        self._children.remove(child)
        self.post("delchild",child)
    def getChildren(self):
        return self._children
