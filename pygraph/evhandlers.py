from evhandler import EvHandler

class MoveEvH(EvHandler):
    def __init__(self,evstack,object,x,y):
        self.evstack=evstack
        self.object=object
	self.startx = x
	self.starty = y
    def mouse_motion(self,x,y):
	x,y = self.object.parent.GetPointer()
        self.object.x,self.object.y=x-self.startx,y-self.starty
        self.object.Redraw()
        return True
    def mouserelease_middle(self):
        self.evstack.remove(self)
        return True
