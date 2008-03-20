#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from pygraph.shapes import Square,Circle

class GraphNode(Square):
    def __init__(self,x,y,w,h):
        Square.__init__(self,x,y,w,h)
        inp_r = h/11.
        stride = h/5
        self.inputs = [Circle(x,y+stride,inp_r,inp_r),Circle(x,y+stride*2,inp_r,inp_r)]
        self.outputs = [Circle(x+w,y+stride,inp_r,inp_r),Circle(x+w,y+stride*2,inp_r,inp_r)]
    def Draw(self,ctx):
        Square.Draw(self,ctx)
        for i,input in enumerate(self.inputs):
            #ctx.move_to (self.x, self.y+6*i)
            input.Draw(ctx)
        for output in self.outputs:
            output.Draw(ctx)
