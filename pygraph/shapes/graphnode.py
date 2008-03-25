#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from pygraph.evhandlers import MoveEvH
from pygraph.graph import *
from pygraph.shapes import Square,Circle,Arrow
import random

colors = [(1,0,0),(0,1,0),(1,1,1),(1,0,1),(0,0,1)]

class ConnEvH(EvHandler):
    def __init__(self,source_c):
        self.source_c=source_c
        self.source=source_c.parent
        self.maingraph=self.source.parent
        arr_x,arr_y=source_c.ToParent(self.maingraph,0,0)
        self.arrow=Arrow(self.maingraph,arr_x,arr_y,arr_x,arr_y,(0,0,0.7))
        self.maingraph.objects[1].append(self.arrow)
        self.maingraph.Redraw()

    def mousepress_left(self):
        x,y=self.maingraph.GetPointer()
        return (not self.maingraph.Test(*self.maingraph.FromLocal(x,y))) or self.maingraph.Propagate(x,y,"connect",self)
        
    def mouse_motion(self,x,y):
        self.arrow.x1,self.arrow.y1=self.maingraph.GetPointer()
        self.maingraph.Redraw()

class NodeConnector(Circle):
    def __init__(self,maingraph,parent,x,y,r,col):
        Circle.__init__(self,parent,x,y,r,col)
        self.maingraph=maingraph
        self.evstack.append(NodeConnectorEvH(self))

class NodeConnectorEvH(EvHandler):
    def __init__(self,nodeconn):
        self.nodeconn=nodeconn
    def mousepress_left(self):
        self.nodeconn.Root().evstack.append(ConnEvH(self.nodeconn))
        return True
    def connect(self,connevh):
        if connevh.source.parent!=self.nodeconn.parent.parent and connevh.source.parent!=self.nodeconn.parent and connevh.source!=self.nodeconn.parent.parent:
            return True
        maingraph=self.nodeconn.Root()
        maingraph.evstack.remove(connevh)
        connevh.maingraph.objects[1].remove(connevh.arrow)
        connevh.maingraph.objects[1].append(NodeConnection(connevh.arrow,connevh.source_c,self.nodeconn))
        maingraph.Redraw()
        return True

class NodeConnection(GraphObject):
    def __init__(self,arrow,source_c,target_c):
        self.arrow=arrow
        self.source=source_c.parent
        self.source_c=source_c
        self.target=target_c.parent
        self.target_c=target_c
    def Draw(self,ctx):
        x0,y0=self.source.ToParent(self.arrow.parent,self.source_c.x,self.source_c.y)
        x1,y1=self.target.ToParent(self.arrow.parent,self.target_c.x,self.target_c.y)
        self.arrow.x,self.arrow.y=x0,y0
        self.arrow.x1,self.arrow.y1=x1,y1
        self.arrow.Draw(ctx)
    def Test(self,x,y):
        return False


class GraphNode(RectCollider,Graph):
    def __init__(self,parent,x,y,w,h):
        self.inp_r = h/15.
        self.stride = h/5
        self.inputs = []
        self.outputs = []
        RectCollider.__init__(self,w+2*self.inp_r,h)
        Graph.__init__(self,parent,x+self.inp_r,y)
        self.objects[1]=[]
        self.objects[0].append(Square(self,self.inp_r,0,w,h))
        ninlets = random.randint(0,4)
        noutlets = random.randint(0,4)
        for i in xrange(ninlets):
            col_idx = random.randint(0,4)
            self.AddInlet(i,colors[col_idx])
        for i in xrange(noutlets):
            col_idx = random.randint(0,4)
            self.AddOutlet(i,colors[col_idx])
        self.evstack.insert(0,GraphNodeEvH(self))

    def AddInlet(self,i,col):
        self.objects[1].append(NodeConnector(self.parent,self,self.inp_r,(1+i)*self.stride,self.inp_r,col))
    def AddOutlet(self,i,col):
        self.objects[1].append(NodeConnector(self.parent,self,self.w-self.inp_r,(1+i)*self.stride,self.inp_r,col))
    def NewNode(self,x,y):
	obj_size = self.scale
	parent = self.parent
        root=self.Root()
	while True:
            obj_size *= parent.scale
            parent = parent.parent
            if parent==root:
                break

        obj_size = 30/obj_size
        self.objects[0].append(GraphNode(self,x-(obj_size/2),y-(obj_size/2),obj_size,obj_size))
        self.Redraw()


class GraphNodeEvH(EvHandler):
    def __init__(self,graphnode):
        self.graphnode=graphnode

    def mousepress_middle(self):
        rootgraph=self.graphnode.Root()
        maingraph=self.graphnode.parent
        x,y=self.graphnode.GetPointer()
        rootgraph.evstack.append(MoveEvH(self.graphnode,x,y))
        maingraph.objects[0].remove(self.graphnode)
        maingraph.objects[0].append(self.graphnode)
        maingraph.Redraw()
        return True

    def keypress_c(self):
        x,y=self.graphnode.GetPointer()
        self.graphnode.NewNode(x,y)
        return True


