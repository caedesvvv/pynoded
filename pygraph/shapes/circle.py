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
        print "draw square"
        ctx.set_source_rgb(*self.col)
        linewidth,_ = ctx.device_to_user_distance(2.,2.)
        ctx.set_line_width(linewidth)
        ctx.set_source_rgb( 1, 1, 1)
        ctx.arc (self.x, self.y, self.w, 0, 2 * math.pi)
        ctx.fill()
        ctx.stroke()
        ctx.set_source_rgb( 0,0,0)
        ctx.arc (self.x, self.y, self.w, 0, 2 * math.pi)
        ctx.stroke()

