import uuid

from meta import ClassRegistry
from basemodel import SubscribableModel

def LoadModel(objs,reqclsname):
    retobj = []
    objects = {}
    tounref = []
    unrefchilds = []
    # load objects
    for objid,obj in objs.iteritems():
        clsname,objuuid = objid.split("#")
        cls = ClassRegistry[clsname]
        newobj = cls()
        if clsname == reqclsname:
            retobj.append(newobj)
        newobj.uuid = uuid.UUID(objuuid)
        objects[objuuid] = newobj
        children = obj.pop("children")
        if len(children):
            unrefchilds.append([newobj,children])
        for prop,value in obj.iteritems():
            if isinstance(value,str) and value.startswith("uuid:"):
                try:
                    value = objects[value[5:]]
                except:
                    tounref.append([newobj,prop])
            newobj.setProperty(prop,value)
    # unref properties
    for newobj2,prop in tounref:
        val = newobj2.getProperty(prop)
        val = objects[val[5:]]
        newobj2.setProperty(prop,val)
    # unref children
    for newobj,children in unrefchilds:
        for child in children:
            newobj.addChild(objects[child])
    return retobj

def SaveModel(model):
    # prepare struct
    props = { "children" : map(lambda s: str(s.uuid),model.getChildren()) }
    obj = {str(model.__class__.__name__)+"#"+str(model.uuid): props}
    # dereference properties
    for prop,value in model._props.iteritems():
        if isinstance(value,SubscribableModel):
            props[prop] = "uuid:"+str(value.uuid)
        else:
            props[prop] = value
    return obj

