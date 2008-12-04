from collections import defaultdict

ClassRegistry = {}
_PendingBuilderInfo = defaultdict(set)

class Property(object):
    def __init__(self,proptype,default):
        self._proptype = proptype
        self._default = default
        # self.name = None # XXX has to be set externally !!
    def __set__(self,obj,val):
        obj.setProperty(self.name,val)
    def __fget__(self,obj):
        return obj.getProperty(self.name)

class SubscribableModelMeta(type):
    def __new__(cls, name, bases, dct):
        acls =  type.__new__(cls, name, bases, dct)
        ClassRegistry[name] = acls
        # XXX some uglyness to avoid putting the name in the
        # Property constructor.
        for propname,obj in dct.iteritems():
            if isinstance(obj,Property):
                obj.name = propname
        # make sure builds is a set
        acls.builds = set(acls.builds)
        # fill in another classes builds using class builtby
        for builder_name in acls.builtby:
            if builder_name in ClassRegistry:
                anothercls = ClassRegistry[builder_name]
                anothercls.builds.add(name)
            else:
                _PendingBuilderInfo[builder_name].add(name)
        # check to see if we had built by subscriptions pending
        if name in _PendingBuilderInfo:
            for built_name in _PendingBuilderInfo[name]:
                acls.builds.add(built_name)
            builder_info.pop(name)
        return acls

