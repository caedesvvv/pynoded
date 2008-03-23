#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from pygraph.gobject import *
from pygraph.shapes import Square,Circle
import random

colors = [(1,0,0),(0,1,0),(1,1,1),(1,0,1),(0,0,1)]

class GraphNode(Square):
    def __init__(self,mainmap,x,y,w,h):
        Square.__init__(self,x,y,w,h)
        self.mainmap=mainmap
        self.inp_r = h/15.
        self.stride = h/5
        self.inputs = []
        self.outputs = []
        ninlets = random.randint(0,4)
        noutlets = random.randint(0,4)
        for i in xrange(ninlets):
            col_idx = random.randint(0,4)
            self.AddInlet(colors[col_idx])
        for i in xrange(noutlets):
            col_idx = random.randint(0,4)
            self.AddOutlet(colors[col_idx])
    def AddInlet(self,col):
        self.inputs.append(Circle(0,0,self.inp_r,self.inp_r,col))
    def AddOutlet(self,col):
        self.outputs.append(Circle(0,0,self.inp_r,self.inp_r,col))
    def Draw(self,ctx):
        Square.Draw(self,ctx)
        ctx.save()
        ctx.translate(self.x,self.y)
        for i,input in enumerate(self.inputs):
            ctx.translate(0,self.stride)
            input.Draw(ctx)
        ctx.restore()
        ctx.save()
        ctx.translate(self.x+self.w,self.y)
        for output in self.outputs:
            ctx.translate(0,self.stride)
            output.Draw(ctx)
        ctx.restore()
    def mousepress_middle(self):
        self.mainmap.evstack.stack.append(MoveEvH(self.mainmap,self))
        self.mainmap.objects.remove(self)
        self.mainmap.objects.append(self)
        self.mainmap.queue_draw()
        return True

class MoveEvH(EvHandler):
    def __init__(self,mainmap,object):
        self.mainmap=mainmap
        self.object=object
    def mouse_motion(self,x,y):
        self.object.x,self.object.y=self.mainmap.Screen2Surface(x,y)
        self.mainmap.queue_draw()
        return True
    def mouserelease_middle(self):
        self.mainmap.evstack.stack.remove(self)
        return True
