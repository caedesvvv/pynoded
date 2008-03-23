
class EvHandler(object):
    pass

class EvStack(EvHandler):
    def __init__(self):
        self.stack=[]
    def __getattr__(self,name):
        def attr(*args):
            for x in reversed(self.stack):
                if x and getattr(x,name,False) and getattr(x,name)(*args):
                    return True
            return False
        return attr
