#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from pygraph.evhandlers import MoveEvH
from pygraph.graph import *
from pygraph.shapes import Square,Circle,Arrow
import random

colors = [(1,0,0),(0,1,0),(1,1,1),(1,0,1),(0,0,1)]

class ConnEvH(EvHandler):
    def __init__(self,maingraph,source):
        self.maingraph=maingraph
        self.source=source
        self.arrow=Arrow((0,0,0.7),source.x)
    def mousepress_left(self):
        print "en connevh"
        self.maingraph.Propagate("connect",self.source)
    def mouse_motion(self,x,y):
        self.maingraph.queue_draw()
        
class NodeConnector(Circle):
    def __init__(self,maingraph,x,y,w,h,col):
        Circle.__init__(self,x,y,w,h,col)
        self.maingraph=maingraph
    def mousepress_left(self):
        print "en nodeconnector"
        self.maingraph.evstack.stack.append(ConnEvH(self.maingraph,self))
    def connect(self,source):
        print "en connect"
        self.maingraph.evstack.stack=filter(lambda x: isinstance(x,ConnEvH),self.maingraph.evstack.stack)
        print source,self

class GraphNode(Graph):
    def __init__(self,maingraph,x,y,w,h):
        Graph.__init__(self)
        self.x=x
        self.y=y
        self.w=w
        self.objects.append(Square(0,0,w,h))
        self.maingraph=maingraph
        self.inp_r = h/15.
        self.stride = h/5
        self.inputs = []
        self.outputs = []
        ninlets = random.randint(0,4)
        noutlets = random.randint(0,4)
        for i in xrange(ninlets):
            col_idx = random.randint(0,4)
            self.AddInlet(i,colors[col_idx])
        for i in xrange(noutlets):
            col_idx = random.randint(0,4)
            self.AddOutlet(i,colors[col_idx])
    def Test(self,x,y):
        return Graph.Test(self,x-self.x,y-self.y)
    def AddInlet(self,i,col):
        self.objects.append(NodeConnector(self.maingraph,0,(1+i)*self.stride,self.inp_r,self.inp_r,col))
    def AddOutlet(self,i,col):
        self.objects.append(NodeConnector(self.maingraph,self.w,(1+i)*self.stride,self.inp_r,self.inp_r,col))
    def Draw(self,ctx):
        ctx.save()
        ctx.translate(self.x,self.y)
        Graph.Draw(self,ctx)
        ctx.restore()
    def mousepress_middle(self):
        self.maingraph.evstack.stack.append(MoveEvH(self.maingraph,self))
        self.maingraph.objects.remove(self)
        self.maingraph.objects.append(self)
        self.maingraph.queue_draw()
        return True

    def Propagate(self,event,*args):
        x,y=self.maingraph.GetPointer()
        return Graph.Propagate(self,x,y,event,*args)

    def mousepress_left(self):
        return self.Propagate("mousepress_left")
    def connect(self,source):
        return self.Propagate("connect",source)
    def keypress_c(self):
        if not self.Propagate("keypress_c"):
            self.maingraph.NewNode(self)
            return True


