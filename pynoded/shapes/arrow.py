"""
Arrow shapes
"""

from pynoded.graph import GraphObject
from math import atan2,pi
from cubicspline import cubicspline
from numpy import array

class Arrow(GraphObject):
    """
    An arrow connecting two objects.
    """
    def __init__(self,parent,x0,y0,x1,y1,color):
        GraphObject.__init__(self,parent,x0,y0)
        self.x1=x1
        self.y1=y1
        self.color=color
        self.maxdist = 3

    def Draw_(self, ctx):
        x1,y1=self.ToLocal(self.x1, self.y1)
        ctx.set_line_width(1)
        linewidth,_ = ctx.device_to_user_distance(1., 1.)
        ctx.set_line_width(linewidth)
        ctx.set_source_rgb(*self.color)
        ctx.move_to(0,0)
        dist = abs(complex(x1, y1))
        elast = dist/2.0
        ctx.curve_to(elast, 0, x1-elast, y1, x1, y1)
        ctx.stroke()
        data = [[float(elast), float(0)],
                [float(x1-elast), float(y1)],
                [float(x1), float(y1)],
                [0, 0]]
        data = array(data)
        time, val = cubicspline(data, 123)
        if linewidth > self.maxdist:
            return
        ctx.move_to(x1, y1)
        # following is to draw the arrow in direction of line
        # but now we're drawing the in/out tangential, so not needed
        # angle=atan2(0,x1)
        # ctx.rotate(angle)
        ctx.rel_line_to(-6*linewidth,0)
        ctx.rel_line_to(0,2*linewidth)
        ctx.rel_line_to(6*linewidth,-2*linewidth)
        ctx.rel_line_to(-6*linewidth,-2*linewidth)
        ctx.rel_line_to(0,2*linewidth)
        ctx.fill_preserve()
        ctx.stroke()

    def Test(self,x,y):
        return False
