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
        self.maingraph=source_c.maingraph
        self.source=source_c.parent
        self.source_c=source_c
        self.arrow=Arrow((0,0,0.7),source.x+source_c.x,source.y+source_c.y,0,0)
        self.maingraph.objects[1].append(self.arrow)

    def mousepress_left(self):
        x,y=self.maingraph.GetPointer()
        return self.maingraph.Propagate(x,y,"connect",self)
        
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
        self.nodeconn.maingraph.evstack.append(ConnEvH(self.nodeconn))
        return True
    def connect(self,connevh):
        self.nodeconn.maingraph.evstack.remove(connevh)
        self.nodeconn.maingraph.objects[1].remove(connevh.arrow)
        self.nodeconn.maingraph.objects[1].append(NodeConnection(connevh.arrow,connevh.source_connector,self.nodeconn))
        self.nodeconn.Redraw()
        return True

class NodeConnection(GraphObject):
    def __init__(self,arrow,source_c,target_c):
        self.arrow=arrow
        self.source=source_c.parent
        self.source_c=source_c
        self.target=target_c.parent
        self.target_c=target_c
    def Draw(self,ctx):
        self.arrow.x=self.source.x+self.source_c.x
        self.arrow.y=self.source.y+self.source_c.y
        self.arrow.x1=self.target.x+self.target_c.x
        self.arrow.y1=self.target.y+self.target_c.y
        self.arrow.Draw(ctx)



class GraphNode(RectCollider,Graph):
    def __init__(self,parent,x,y,w,h):
        Graph.__init__(self,parent,x,y)
        RectCollider.__init__(self,w,h)
        self.objects[1]=[]
        self.objects[0].append(Square(self,0,0,w,h))
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
        self.evstack.insert(0,GraphNodeEvH(self))

    def AddInlet(self,i,col):
        self.objects[1].append(NodeConnector(self.parent,self,0,(1+i)*self.stride,self.inp_r,col))
    def AddOutlet(self,i,col):
        self.objects[1].append(NodeConnector(self.parent,self,self.w,(1+i)*self.stride,self.inp_r,col))
    def NewNode(self,x,y):
        obj_size = 30/self.scale
        self.objects[0].append(GraphNode(self,x-(obj_size/2),y-(obj_size/2),obj_size,obj_size))
        self.Redraw()


class GraphNodeEvH(EvHandler):
    def __init__(self,graphnode):
        self.graphnode=graphnode

    def mousepress_middle(self):
        self.graphnode.parent.evstack.append(MoveEvH(self.graphnode.parent.evstack,self.graphnode))
        self.graphnode.parent.objects[0].remove(self.graphnode)
        self.graphnode.parent.objects[0].append(self.graphnode)
        self.graphnode.parent.queue_draw()
        return True

    def keypress_c(self):
        x,y=self.graphnode.GetPointer()
        self.graphnode.NewNode(x,y)
        return True


