#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from pygraph.graph import GraphObject,RectCollider
import math

class Circle(RectCollider,GraphObject):
    def __init__(self,parent,x,y,r,col=(0.1,0.1,0.1)):
        GraphObject.__init__(self,parent,x-r,y-r)
        RectCollider.__init__(self,2*r,2*r)
        self.col = col
        self.r=r

    def Draw_(self,ctx):
        linewidth,_ = ctx.device_to_user_distance(2.,2.)
        ctx.set_line_width(linewidth)
        ctx.set_source_rgb(*self.col)
        ctx.arc (0, 0, self.r, 0, 2 * math.pi)
        ctx.fill_preserve()
        ctx.set_source_rgb( 0,0,0)
        ctx.stroke()

