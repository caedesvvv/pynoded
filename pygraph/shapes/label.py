"""
Label shapes
"""

from pygraph.graph import GraphObject,RectCollider
from cairo import FONT_SLANT_NORMAL,FONT_WEIGHT_NORMAL

class Label(RectCollider,GraphObject):
    """
    A simple label
    """
    def __init__(self,parent,x,y,w,h,col=(1.0,1.0,1.0),name=""):
        """
        Constructor for Label
        @param parent: parent graphobject.
        @param x: x position relative to parent
        @param y: y position relative to parent
        @param w: width of the label
        @param h: height of the label
        @param col: color for the label
        @param name: text for the label
        """
        GraphObject.__init__(self,parent,x,y)
        RectCollider.__init__(self,w,h)
        self.col = col
        self.name = name
        self.maxdist = 4

    def Draw_(self,ctx):
        linewidth,_ = ctx.device_to_user_distance(1.,1.)
        if linewidth>=self.maxdist:
            return
        ctx.select_font_face("Sans",FONT_SLANT_NORMAL,FONT_WEIGHT_NORMAL)
        ctx.set_font_size(self.h*0.9)
        ctx.set_source_rgb(*self.col)
        linewidth,_ = ctx.device_to_user_distance(2.,2.)
        ctx.set_line_width(linewidth)
        #ctx.rectangle(0,0,self.w,self.h)
        #ctx.set_source_rgb( *self.col ) 
        #ctx.fill_preserve( )
        ctx.set_source_rgb( 0, 0, 0) 
        ctx.move_to (0,self.h);
        ctx.line_to(self.w,self.h)
        ctx.move_to (3, self.h*0.9);
        ctx.show_text(self.name)
        ctx.stroke()
