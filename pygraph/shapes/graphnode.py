#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from pygraph.shapes import Square,Circle

class GraphNode(Square):
    def __init__(self,x,y,w,h):
        Square.__init__(self,x,y,w,h)
        inp_r = h/11.
        stride = h/5
        self.stride = stride
        self.inputs = [Circle(0,0,inp_r,inp_r),Circle(0,0,inp_r,inp_r)]
        self.outputs = [Circle(0,0,inp_r,inp_r),Circle(0,0,inp_r,inp_r)]
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
