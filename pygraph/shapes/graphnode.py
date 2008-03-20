#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from pygraph.shapes import Square

class GraphNode(Square):
    def __init__(self,x,y,w,h):
        Square.__init__(self,x,y,w,h)

