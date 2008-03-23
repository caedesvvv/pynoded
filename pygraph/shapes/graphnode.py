#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from pygraph.evhandlers import MoveEvH
from pygraph.graph import *
from pygraph.shapes import Square,Circle,Arrow
import random

colors = [(1,0,0),(0,1,0),(1,1,1),(1,0,1),(0,0,1)]

class ConnEvH(EvHandler):
    def __init__(self,maingraph,source,source_connector):
        self.maingraph=maingraph
        self.source=source
        self.source_connector=source_connector
        self.arrow=Arrow((0,0,0.7),source.x+source_connector.x,source.y+source_connector.y,0,0)
        self.maingraph.objects[1].append(self.arrow)
    def mousepress_left(self):
        x,y=self.maingraph.GetPointer()
        return self.maingraph.Propagate(x,y,"connect",self)
        
    def mouse_motion(self,x,y):
        self.arrow.x1,self.arrow.y1=self.maingraph.GetPointer()
        self.maingraph.queue_draw()

class NodeConnector(Circle):
    def __init__(self,maingraph,parent,x,y,w,h,col):
        Circle.__init__(self,x,y,w,h,col)
        self.maingraph=maingraph
        self.parent=parent
    def mousepress_left(self):
        self.maingraph.evstack.stack.append(ConnEvH(self.maingraph,self.parent,self))
        return True
    def connect(self,connevh):
        self.maingraph.evstack.stack.remove(connevh)
        self.maingraph.objects[1].remove(connevh.arrow)
        self.maingraph.objects[1].append(NodeConnection(connevh.arrow,connevh.source,connevh.source_connector,self.parent,self))
        self.maingraph.queue_draw()
        return True

class NodeConnection(GraphObject):
    def __init__(self,arrow,source,source_c,target,target_c):
        self.arrow=arrow
        self.source=source
        self.source_c=source_c
        self.target=target
        self.target_c=target_c
    def Draw(self,ctx):
        self.arrow.x0=self.source.x+self.source_c.x
        self.arrow.y0=self.source.y+self.source_c.y
        self.arrow.x1=self.target.x+self.target_c.x
        self.arrow.y1=self.target.y+self.target_c.y
        self.arrow.Draw(ctx)

class GraphNode(Graph):
    def __init__(self,maingraph,x,y,w,h):
        Graph.__init__(self)
        self.objects[1]=[]
        self.x=x
        self.y=y
        self.w=w
        self.objects[0].append(Square(0,0,w,h))
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
        self.objects[1].append(NodeConnector(self.maingraph,self,0,(1+i)*self.stride,self.inp_r,self.inp_r,col))
    def AddOutlet(self,i,col):
        self.objects[1].append(NodeConnector(self.maingraph,self,self.w,(1+i)*self.stride,self.inp_r,self.inp_r,col))
    def Draw(self,ctx):
        ctx.save()
        ctx.translate(self.x,self.y)
        Graph.Draw(self,ctx)
        ctx.restore()
    def mousepress_middle(self):
        self.maingraph.evstack.stack.append(MoveEvH(self.maingraph,self))
        self.maingraph.objects[0].remove(self)
        self.maingraph.objects[0].append(self)
        self.maingraph.queue_draw()
        return True

    def Propagate(self,event,*args):
        x,y=self.maingraph.GetPointer()
        return Graph.Propagate(self,x-self.x,y-self.y,event,*args)
                         
    def mousepress_left(self):
        return self.Propagate("mousepress_left")
    def connect(self,source):
        return self.Propagate("connect",source)
    def keypress_c(self):
        if not self.Propagate("keypress_c"):
            self.maingraph.NewNode(self)
            return True


