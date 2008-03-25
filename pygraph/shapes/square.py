#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from pygraph.graph import GraphObject,RectCollider

class Square(RectCollider,GraphObject):
    def __init__(self,parent,x,y,w,h,col=(0.1,0.1,0.1)):
        GraphObject.__init__(self,parent,x,y)
        RectCollider.__init__(self,w,h)
        self.col = col

    def Draw_(self,ctx):
        ctx.set_source_rgb(*self.col)
        linewidth,_ = ctx.device_to_user_distance(2.,2.)
        ctx.set_line_width(linewidth)
        ctx.rectangle(0,0,self.w,self.h)
        ctx.set_source_rgb( 1, 1, 1) 
        ctx.fill_preserve( )
        ctx.set_source_rgb( 0, 0, 0) 
        ctx.stroke()
