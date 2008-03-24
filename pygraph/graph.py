from evhandler import EvHandler,EvStack

class Drawable(object):
    def __init__(self,x,y,scale=1.0):
        self.x=x
        self.y=y
        self.scale=scale

    def Draw(self,ctx):
        ctx.save()
        ctx.translate(self.x,self.y)
        ctx.scale(self.scale,self.scale)
        self.Draw_(ctx)
        ctx.restore()

    def ToLocal(self,x,y):
        return ((x/self.scale)-self.x,(y/self.scale)-self.y)

    def FromLocal(self,x,y):
        return (self.x+x*self.scale,self.y+y*self.scale)

    def Draw_(self,ctx):
        pass

class Collider(object):
     def Test(self,x,y):
         raise "Not implemented!"

class RectCollider(Collider):
    def __init__(self,w,h):
        self.w=w
        self.h=h

    def Test(self,x,y):
        return x>=self.x and x<=self.x+self.w and y>=self.y and y<=self.y+self.h

class GraphObject(Drawable,Collider):
    def __init__(self,parent,x,y,scale=1.0):
        self.parent=parent
        Drawable.__init__(x,y,scale)
        self.evstack=EvStack()
    def GetPointer(self):
        return self.ToLocal(*self.parent.GetPointer())
    def Redraw(self):
        self.parent.Redraw()

class Graph(GraphObject):
    def __init__(self,parent,x,y,scale=1.0):
        GraphObject.__init__(self,parent,x,y,scale)
        self.objects={0:[]}
        self.evstack.append(PropagateEvH(self))

    def Draw_(self,ctx):
        for prio in self.objects.values():
            for obj in prio:
                obj.Draw(ctx)

    def Propagate(self,x,y,event,*args):
        o=self.ObjectAt(x,y)
        return o and getattr(o.evstack,event,False) and getattr(o.evstack,event)(*args)

    def ObjectAt(self,x,y):
        x,y=self.ToLocal(x,y)
        for prio in reversed(self.objects.values()):
            for o in reversed(prio):
                if o.Test(x,y):
                    return o

class PropagateEvH(EvHandler):
    def __init__(self,graph):
        self.graph=graph

    def __getattr__(self,name):
        return lambda x,y,*args: self.graph.Propagate(x,y,name,*args)
