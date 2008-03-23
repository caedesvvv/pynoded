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

    def ObjectAt(self,x,y):
        for o in reversed(self.objects):
            if o.Test(x,y):
                return o
