import uuid
import dMVC.model
from meta import SubscribableModelMeta,ClassRegistry

gdict = {}

########################################################
# dmvc model
class DMVCSubscribableModel(dMVC.model.Model):
    __metaclass__ = SubscribableModelMeta
    def __init__(self, instance_uuid=None):
        dMVC.model.Model.__init__(self)
        self._evhs = []
        self._children = []
        self._props = {}
        if instance_uuid:
            self.uuid = uuid.UUID(instance_uuid)
        else:
            self.uuid = uuid.uuid1()

    def variablesToSerialize(self):
        return ['_evhs']

    def copyfrom(self, other):
        self._evhs = []
        self._children = other._children
        self._props = other._props
        self.uuid = other.uuid
        self.invalidate()
    def new(self, clsname, *args, **kwargs):
        return ClassRegistry[clsname](*args, **kwargs)
    def setProperty(self,name,value):
        if self._props.get(name,None) == value:
            return
        else:
            self._props[name] = value
        self.triggerEvent("propertychange",name=name,value=value)
    def getProperty(self,name):
        return self._props[name]
    def getProperties(self):
        return self._props.keys()
    def addChild(self, child):
        self._children.append(child)
        self.triggerEvent("addchild",child=child)
    def delChild(self, child):
        self._children.remove(child)
        self.triggerEvent("delchild",child=child)
    def getChildren(self):
        return self._children
    @dMVC.model.localMethod
    def doInvalidate(self,evt):
        self.post("invalidate")
    def invalidate(self):
        self.triggerEvent("invalidate")
    # XXX TODO::: ------------------
    @dMVC.model.localMethod
    def getAddChild(self, evt):
        params = evt.getParams()
        self.post("addchild",params["child"])
    @dMVC.model.localMethod
    def getDelChild(self, evt):
        params = evt.getParams()
        self.post("delchild",params["child"])
    @dMVC.model.localMethod
    def getChangeProperty(self, evt):
        params = evt.getParams()
        self.post("propertychange",params["name"],params["value"])
    @dMVC.model.localMethod
    def subscribe(self, evh):
        self.subscribeEvent("addchild",self.getAddChild)
        self.subscribeEvent("invalidate",self.doInvalidate)
        self.subscribeEvent("delchild",self.getDelChild)
        self.subscribeEvent("propertychange",self.getChangeProperty)
        self._evhs.append(evh)
    @dMVC.model.localMethod
    def unsubscribe(self, evh):
        self._evhs.remove(evh)
    @dMVC.model.localMethod
    def post(self, name, *args):
        for evh in self._evhs:
            if hasattr(evh,name):
                getattr(evh,name)(*args)

