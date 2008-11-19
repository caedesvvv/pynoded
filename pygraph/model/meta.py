ClassRegistry = {}

class SubscribableModelMeta(type):
    def __new__(cls, name, bases, dct):
        acls =  type.__new__(cls, name, bases, dct)
        ClassRegistry[name] = acls
        return acls

