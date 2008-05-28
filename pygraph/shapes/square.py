"""
Square shapes
"""

from pygraph.graph import GraphObject,RectCollider

class Square(RectCollider,GraphObject):
    """
    An outlined and color filled rectangle.
    """
    def __init__(self,parent,x,y,w,h,col=(1,1,1)):
        """
        Constructor for Square
        @param parent: parent graphobject.
        @param x: x position relative to parent
        @param y: y position relative to parent
        @param w: width of the square
        @param h: height of the square
        @param col: color for the square
        """
        GraphObject.__init__(self,parent,x,y)
        RectCollider.__init__(self,w,h)
        self.col = col

    def Draw_(self,ctx):
        ctx.set_source_rgb(*self.col)
        linewidth,_ = ctx.device_to_user_distance(2.,2.)
        ctx.set_line_width(linewidth)
        ctx.rectangle(0,0,self.w,self.h)
        ctx.set_source_rgb( *self.col ) 
        ctx.fill_preserve( )
        ctx.set_source_rgb( 0, 0, 0) 
        ctx.stroke()

class FancySquare(Square):
    """
    A rectangle with smoothed borders.
    """
    def __init__(self,parent,x,y,w,h,col=(1,1,1)):
        """
        Constructor for FancySquare
        @param parent: parent graphobject.
        @param x: x position relative to parent
        @param y: y position relative to parent
        @param w: width of the square
        @param h: height of the square
        @param col: color for the square
        """
        Square.__init__(self,parent,x,y,w,h,col)
        self.maxdist = 4
        self.smooth = 10

    def Draw_(self,ctx):
        linewidth,_ = ctx.device_to_user_distance(1.,1.)
        if linewidth > self.maxdist:
            Square.Draw_(self,ctx)
            return
        ctx.set_source_rgb(*self.col)
        linewidth,_ = ctx.device_to_user_distance(2.,2.)
        f = self.smooth
        ctx.set_line_width(linewidth)
        ctx.move_to (f,0)
        ctx.line_to(self.w-f,0) # top
        ctx.curve_to(self.w,0,self.w,0,self.w,f)
        ctx.line_to(self.w,self.h-f) # right
        ctx.curve_to(self.w,self.h,self.w,self.h,self.w-f,self.h)
        ctx.line_to(f,self.h) # bottom
        ctx.curve_to(0,self.h,0,self.h,0,self.h-f)
        ctx.line_to(0,f) # left
        ctx.curve_to(0,0,0,0,f,0)
        ctx.close_path()

        ctx.set_source_rgb( *self.col ) 
        ctx.fill_preserve( )
        ctx.set_source_rgb( 0, 0, 0) 
        ctx.stroke()
