"""
Event Handler Base Classes
"""
class EvHandler(object):
    """
    Base class for all Event Handlers.
    """
    pass

class EvStack(EvHandler,list):
    """
    An event stack.
    """
    def __init__(self):
        list.__init__(self)
    def __getattr__(self,name):
        def attr(*args):
            for x in reversed(self):
                if x and getattr(x,name,False) and getattr(x,name)(*args):
                    return True
            return False
        return attr
