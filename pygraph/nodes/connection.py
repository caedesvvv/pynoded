"""
Graph connections
"""
from pygraph.graph import *
from pygraph.shapes import Circle,Arrow

class ConnEvH(EvHandler):
    """
    Base connection event handler, for broadcasting connections.
    """
    def __init__(self,source_c):
        self.source_c=source_c
        self.source=source_c.parent
        self.maingraph=self.source.parent
        arr_x,arr_y=source_c.ToParent(self.maingraph,0,0)
        self.arrow=Arrow(self.maingraph,arr_x,arr_y,arr_x,arr_y,(0,0,0.7))
        self.maingraph.objects[1].append(self.arrow)
        self.maingraph.Redraw()

    def mousepress_left(self):
        x,y=self.maingraph.GetPointer()
        return (not self.maingraph.Test(*self.maingraph.FromLocal(x,y))) or self.maingraph.Propagate(x,y,"connect",self)
        
    def mouse_motion(self,x,y):
        self.arrow.x1,self.arrow.y1=self.maingraph.GetPointer()
        self.maingraph.Redraw()

class NodeConnectorEvH(EvHandler):
    """
    Base connection event handler, for incoming connections.
    """
    def __init__(self,nodeconn):
        self.nodeconn=nodeconn
    def mousepress_left(self):
        self.nodeconn.Root().evstack.append(ConnEvH(self.nodeconn))
        return True
    def connect(self,connevh):
        if connevh.source.parent!=self.nodeconn.parent.parent and connevh.source.parent!=self.nodeconn.parent and connevh.source!=self.nodeconn.parent.parent:
            return True
        if not connevh.source_c.CanConnect(self.nodeconn):
            return True
        maingraph=self.nodeconn.Root()
        maingraph.evstack.remove(connevh)
        connevh.maingraph.objects[1].remove(connevh.arrow)
        newcon = NodeConnection(connevh.arrow,connevh.source_c,self.nodeconn)
        connevh.maingraph.objects[1].append(newcon) # add arrow to graph
        connevh.source_c.outputs.append(newcon) # add connection to source
        self.nodeconn.inputs.append(newcon) # add conection to target input
        maingraph.Redraw()
        return True

class NodeConnector(Circle):
    """
    A node connector.
    """
    def __init__(self,maingraph,parent,x,y,r,col,evh=NodeConnectorEvH):
        Circle.__init__(self,parent,x,y,r,col)
        self.maingraph=maingraph
        self.evstack.append(evh(self))
        self.inputs = []
        self.outputs = []
    def CanConnect(self):
        return True
    def GetNextNodes(self):
        nodes = []
        for output in self.outputs:
            nodes.append(output.target)
        return nodes
    def GetPreviousNodes(self):
        nodes = []
        for input in self.inputs:
            nodes.append(input.source)
        return nodes
class NodeConnection(GraphObject):
    """
    A connection between two connectors.
    """
    def __init__(self,arrow,source_c,target_c):
        self.arrow=arrow
        self.source=source_c.parent
        self.source_c=source_c
        self.target=target_c.parent
        self.target_c=target_c
    def Draw(self,ctx):
        x0,y0=self.source.ToParent(self.arrow.parent,self.source_c.x,self.source_c.y)
        x1,y1=self.target.ToParent(self.arrow.parent,self.target_c.x,self.target_c.y)
        self.arrow.x,self.arrow.y=x0,y0
        self.arrow.x1,self.arrow.y1=x1,y1
        self.arrow.Draw(ctx)
    def Test(self,x,y):
        return False


