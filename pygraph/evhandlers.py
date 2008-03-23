from evhandler import EvHandler
class PropagateEvH(EvHandler):
    def __init__(self,graph):
        self.graph=graph

    def __getattr__(self,name):
        return lambda *args: self.graph.Propagate(name,*args)

class MoveEvH(EvHandler):
    def __init__(self,maingraph,object):
        self.maingraph=maingraph
        self.object=object
    def mouse_motion(self,x,y):
        self.object.x,self.object.y=self.maingraph.Screen2Surface(x,y)
        self.maingraph.queue_draw()
        return True
    def mouserelease_middle(self):
        self.maingraph.evstack.stack.remove(self)
        return True
