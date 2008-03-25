from evhandler import EvHandler

class MoveEvH(EvHandler):
    def __init__(self,evstack,object):
        self.evstack=evstack
        self.object=object
    def mouse_motion(self,x,y):
        self.object.x,self.object.y=self.object.parent.ToLocal(x,y)
        self.object.Redraw()
        return True
    def mouserelease_middle(self):
        self.evstack.remove(self)
        return True
