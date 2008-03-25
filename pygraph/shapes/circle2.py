#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from pygraph.shapes import GraphObject
import math

class Circle(GraphObject):
    def __init__(self,x,y,w,h,col=(0.1,0.1,0.1)):
        GraphObject.__init__(self)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.col = col
    def Draw(self,ctx):
        linewidth,_ = ctx.device_to_user_distance(2.,2.)
        ctx.set_line_width(linewidth)
        ctx.set_source_rgb(*self.col)
        ctx.arc (self.x, self.y, self.w, 0, 2 * math.pi)
        ctx.fill_preserve()
        ctx.set_source_rgb( 0,0,0)
        ctx.stroke()

        col = map(lambda s: s*0.8,self.col)
        ctx.set_source_rgb(*col)
        ctx.arc (self.x+self.w/4., self.y+self.h/4., self.w/2.0, 0, 2 * math.pi)
        ctx.fill()
        ctx.stroke()

