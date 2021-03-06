"""
Base graph objects
"""

from evh.base import EvHandler,EvStack
from math import *

class Drawable(object):
    """
    Base class for drawable objects.
    """
    def __init__(self,x,y,scale=1.0):
        self.x=x
        self.y=y
        self.scale=scale

    def Draw(self,ctx):
        ctx.save()
        ctx.scale(self.scale,self.scale)
        ctx.translate(self.x,self.y)
        self.Draw_(ctx)
        ctx.restore()

    def ToLocal(self,x,y):
        return ((x/self.scale)-self.x,(y/self.scale)-self.y)

    def FromLocal(self,x,y):
        return (self.x+x*self.scale,self.y+y*self.scale)

    def Draw_(self,ctx):
        """
        Main method to do the cairo drawing of the object.
        This is the main function drawable objects have to override.
        @param ctx: cairo context
        """
        pass

class Collider(object):
     """
     Base class for colliders.
     """
     def Test(self,x,y):
         raise repr(self),"Not implemented!"

class CircleCollider(Collider):
    """
    A circle collider.
    """
    def __init__(self,r):
        self.r=r
    def Test(self,x,y):
        return sqrt((x-self.x)**2+(y-self.y)**2)<=self.r
    
class RectCollider(Collider):
    """
    A rect collider.
    """
    def __init__(self,w,h):
        self.w=w
        self.h=h

    def Test(self,x,y):
        return x>=self.x and x<=self.x+self.w and y>=self.y and y<=self.y+self.h

class GraphObject(Drawable,Collider):
    """
    Base class for graph objects.
    """
    def __init__(self,parent,x,y,scale=1.0):
        if parent:
            self.parent=parent
        Drawable.__init__(self,x,y,scale)
        self.evstack=EvStack()
    def GetPointer(self):
        return self.ToLocal(*self.parent.GetPointer())
    def Redraw(self):
        self.parent.Redraw()
    def ToParent(self,obj,x,y):
        if obj==self:
            return (x,y)
        else:
            return self.parent.ToParent(obj,*self.FromLocal(x,y))
    def Root(self):
        return self.parent.Root()

class Graph(GraphObject):
    """
    A graph capable of containing connected objects.
    """
    def __init__(self,parent,x,y,scale=1.0):
        GraphObject.__init__(self,parent,x,y,scale)
        self.evstack.append(PropagateEvH(self))
        self.Clear()

    def Clear(self):
        self.objects=[[],[],[],[]]

    def Draw_(self,ctx):
        for prio in self.objects:
            for obj in prio:
                obj.Draw(ctx)

    def Propagate(self,x,y,event,*args):
        o=self.ObjectAt(x,y)
        return o and getattr(o.evstack,event,False) and getattr(o.evstack,event)(*args)

    def ObjectAt(self,x,y):
        for prio in reversed(self.objects):
            for o in reversed(prio):
                if o.Test(x,y):
                    return o


class MainGraph(Graph):
    """
    Base class for main graphs.
    """
    def __init__(self,*args):
        Graph.__init__(self,*args)
        self.objects[1]=[]

    def Clear(self):
        Graph.Clear(self)
        self.objects[1]=[]

    def Zoom(self,x,y,factor):
        pre_x,pre_y = self.ToLocal(x,y)
        self.scale *=factor
        post_x,post_y = self.ToLocal(x,y)
        self.x,self.y = (self.x+post_x-pre_x,self.y+post_y-pre_y)
        self.Redraw()

    def AddNode(self,obj):
        self.objects[0].append(obj)
        self.Redraw()

    def ToGlobal(self,x,y):
        return (x,y)

    def GetRawPointer(self):
        raise "Not implemented"

    def GetPointer(self):
        return self.ToLocal(*self.RawPointer)

    def Root(self):
        return self

    def Test(self,x,y):
        return True

    def CenteredBB(self,x,y,size):
        # not really needed, but useful in general..
        obj_size = size
        bb = [x-(obj_size/2),y-(obj_size/2),obj_size,obj_size]
        return bb

    RawPointer = property(GetRawPointer)
    Pointer = property(GetPointer)

class PropagateEvH(EvHandler):
    """
    Event handler for propagating to children.
    """
    def __init__(self,graph):
        """
        PropagateEvH Constructor.
        @param graph: graph to which this event handler is attached.
        """
        self.graph=graph

    def __getattr__(self,name):
        x,y=self.graph.GetPointer()
        return lambda *args: self.graph.Propagate(x,y,name,*args)
