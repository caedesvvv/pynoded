from evhandler import EvHandler

class Drawable(object):
    def Draw(self,ctx):
        pass
    def Test(self,x,y):
        pass

class GraphObject(EvHandler,Drawable):
    pass

class Graph(GraphObject):
    def __init__(self):
        self.objects=[]
    def Draw(self,ctx):
        # draw all CairoObjects
        for obj in self.objects:
            obj.Draw(ctx)

    def Test(self,x,y):
        return self.ObjectAt(x,y)!=None

    def Propagate(self,x,y,event,*args):
        o=self.ObjectAt(x,y)
        return o and getattr(o,event,False) and getattr(o,event)(*args)

    def ObjectAt(self,x,y):
        for o in reversed(self.objects):
            if o.Test(x,y):
                return o

