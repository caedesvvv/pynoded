#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from pygraph.graph import GraphObject

class Square(GraphObject):
    def __init__(self,x,y,w,h,col=(0.1,0.1,0.1)):
        GraphObject.__init__(self)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.col = col
    def Draw(self,ctx):
        ctx.set_source_rgb(*self.col)
        linewidth,_ = ctx.device_to_user_distance(2.,2.)
        ctx.set_line_width(linewidth)
        ctx.rectangle(self.x,self.y,self.w,self.h)
        ctx.set_source_rgb( 1, 1, 1) 
        ctx.fill_preserve( )
        ctx.set_source_rgb( 0, 0, 0) 
        ctx.stroke()
    def Test(self,x,y):
        return x>=self.x and x<=self.x+self.w and y>=self.y and y<=self.y+self.h
    def Move(self,x,y):
        self.x=x
        self.y=y

