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

class Drawable(object):
    def Draw(self,ctx):
        pass
    def Test(self,x,y):
        pass

class GObject(EvHandler,Drawable):
    pass

class GObjMap(GObject):
    def __init__(self):
        self.objects=[]

    def Draw(self,ctx):
        # draw all CairoObjects
        for obj in self.objects:
            obj.Draw(ctx)

    def ObjectAt(self,x,y):
        for o in reversed(self.objects):
            if o.Test(x,y):
                return o
