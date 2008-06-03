"""
Miscelaneus Event Handlers
"""

from evhandler import EvHandler

class MoveEvH(EvHandler):
    """
    Event handler for stacking when dragging an object.
    """
    def __init__(self,object,x,y):
        self.evstack=object.Root().evstack
        self.object=object
        self.startx = x
        self.starty = y
    def mouse_motion(self,x,y):
        x,y = self.object.parent.GetPointer()
        if self.object.parent.Test(*self.object.parent.FromLocal(x,y)):
            self.object.x,self.object.y=x-self.startx,y-self.starty
            self.object.Redraw()
        return True
    def mouserelease_middle(self):
        self.evstack.remove(self)
        return True
