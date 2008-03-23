#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from pygraph.graph import GraphObject
from math import atan2

class Arrow(GraphObject):
    def __init__(self,color,x0,y0,x1,y1):
        GraphObject.__init__(self)
        self.x0=x0
        self.x1=x1
        self.y0=y0
        self.y1=y1
        self.color=color
    def Draw(self,ctx):
        ctx.save()
        ctx.set_line_width(1)
        linewidth,_ = ctx.device_to_user_distance(1.,1.)
        ctx.set_line_width(linewidth)
        ctx.set_source_rgb(*self.color)
        ctx.move_to(self.x0,self.y0)
        ctx.line_to(self.x1,self.y1)
        angle=atan2((self.y1-self.y0),(self.x1-self.x0))
        ctx.rotate(angle)
        ctx.rel_line_to(-6,0)
        ctx.rel_line_to(0,3)
        ctx.rel_line_to(6,-3)
        ctx.rel_line_to(-6,-3)
        ctx.rel_line_to(0,3)
        ctx.fill_preserve()
        ctx.stroke()
        ctx.restore()
