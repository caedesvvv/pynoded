
class EvHandler(object):
    pass

class EvStack(EvHandler,list):
    def __init__(self):
        list.__init__(self)
    def __getattr__(self,name):
        def attr(*args):
            for x in reversed(self):
                if x and getattr(x,name,False) and getattr(x,name)(*args):
                    return True
            return False
        return attr
