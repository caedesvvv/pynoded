#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from pygraph.graph import GraphObject
import math

class Circle(GraphObject):
    def __init__(self,x,y,w,h,col=(0.1,0.1,0.1)):
        GraphObject.__init__(self)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.col = col
        self.linewidth= 2

    def Draw(self,ctx):
        self.linewidth,_ = ctx.device_to_user_distance(2.,2.)
        ctx.set_line_width(self.linewidth)
        ctx.set_source_rgb(*self.col)
        ctx.arc (self.x, self.y, self.w, 0, 2 * math.pi)
        ctx.fill_preserve()
        ctx.set_source_rgb( 0,0,0)
        ctx.stroke()
    def Test(self,x,y):
        r=self.linewidth+self.w
        return x>=self.x-r and x<=self.x+r and y>=self.y-r and y<=self.y+r

