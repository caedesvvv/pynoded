"""
Simple base event handlers.
"""

from base import *

class GraphEvH(EvHandler):
    """
    Example graph event handler.
    It can zoom with mouse and keyboard, create new nodes...
    """
    def __init__(self,maingraph):
        self.maingraph=maingraph

    def scroll_up(self):
        x,y=self.maingraph.RawPointer
        self.maingraph.Zoom(x,y,1/0.99)
        
    def keypress_plus(self):
        self.maingraph.Zoom(self.maingraph.Width/2,self.maingraph.Height/2,1/0.99)
        return True

    def scroll_down(self):
        x,y=self.maingraph.RawPointer
        self.maingraph.Zoom(x,y,0.99)

    def keypress_minus(self):
        self.maingraph.Zoom(self.maingraph.Width/2,self.maingraph.Height/2,0.99)
        return True

    def keypress_c(self):
        self.maingraph.NewNode(*self.maingraph.RawPointer)
        return True

    def mousepress_right(self):
        x,y=self.maingraph.RawPointer
        self.maingraph.evstack.append(GraphScrollEvH(self.maingraph,x,y))
        return True

    #def mouse_motion(self,x,y):
    #    return False

    def expose(self):
        self.maingraph.CreateContext()
        self.maingraph.Draw()
        # draw on window
        self.maingraph.Blit()
        return True

class GraphScrollEvH(EvHandler):
    """
    Event handler for scrolling actions (happening between down and up).
    This event handler can handle moving of the main graph based on position.
    """
    def __init__(self,maingraph,initmx,initmy):
        self.maingraph=maingraph
        self.initpos=maingraph.x,maingraph.y
        self.initmx=initmx
        self.initmy=initmy

    def mouse_motion(self,x,y):
        dx,dy=float(x-self.initmx),float(y-self.initmy)
        self.maingraph.x,self.maingraph.y=(self.maingraph.x+dx/self.maingraph.scale,self.maingraph.y+dy/self.maingraph.scale)
        self.initpos=self.maingraph.x,self.maingraph.y
        self.initmx,self.initmy=x,y
        self.maingraph.Redraw()
        return True

    def mousepress_right(self):
        self.maingraph.evstack.remove(self)
        return True

    def mouserelease_right(self):
        self.maingraph.evstack.remove(self)
        return True
