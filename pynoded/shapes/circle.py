"""
Circle shapes
"""

from pynoded.graph import GraphObject,CircleCollider
import math

class Circle(CircleCollider,GraphObject):
    """
    A circle shape.
    """
    def __init__(self,parent,x,y,r,col=(0.1,0.1,0.1)):
        """
        Circle constructor.
        @param parent: parent graphobject.
        @param x: x position relative to parent
        @param y: y position relative to parent
        @param r: radius for the circle
        @param col: color for the circle
        """
        GraphObject.__init__(self,parent,x,y)
        CircleCollider.__init__(self,r)
        self.col = col
        self.r0=r
        self.r=2+self.r0

    def Draw_(self,ctx):
        linewidth,_ = ctx.device_to_user_distance(2.,2.)
        self.r=self.r0+linewidth
        ctx.set_line_width(linewidth)
        ctx.set_source_rgb(*self.col)
        ctx.arc (0, 0, self.r0, 0, 2 * math.pi)
        ctx.fill_preserve()
        ctx.set_source_rgb( 0,0,0)
        ctx.stroke()

