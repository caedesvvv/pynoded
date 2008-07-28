"""
Graph nodes
"""
from pygraph.evh.move import MoveEvH
from pygraph.graph import *
from pygraph.shapes import Square,Label,FancySquare
from pygraph.nodes.connection import NodeConnector
import random

colors = [(1,0,0),(0,1,0),(1,1,1),(1,0,1),(0,0,1)]

INLETS = 1
OUTLETS = 2

class GraphNodeEvH(EvHandler):
    """
    Example graph node event handler.
    """
    def __init__(self,graphnode):
        self.graphnode=graphnode

    def mousepress_middle(self):
        rootgraph=self.graphnode.Root()
        maingraph=self.graphnode.parent
        x,y=self.graphnode.GetPointer()
        rootgraph.evstack.append(MoveEvH(self.graphnode,x,y))
        maingraph.objects[0].remove(self.graphnode)
        maingraph.objects[0].append(self.graphnode)
        maingraph.Redraw()
        return True

    def keypress_c(self):
        x,y=self.graphnode.GetPointer()
        self.graphnode.NewNode(x,y)
        return True

class GraphNode(RectCollider,Graph):
    """
    A simple graph node with a label and left to right inlets and outlets.
    """
    def __init__(self,parent,x,y,w,h,name="",ninlets=None,noutlets=None,evhandler=GraphNodeEvH,col=(1,1,1)):
        """
        Constructor.
        @param parent: parent graphobject.
        @param x: x position relative to parent
        @param y: y position relative to parent
        @param w: width of the square
        @param h: height of the square
        @param name: name of the widget (will be shown on label)
        @param ninlets: if specified this number of inlets will be created
        @param noutlets: if specified this number of outlets will be created
        @param name: name of the widget (will be shown on label)
        @param evhandler: Class to create an event handler from for this object.
        @param col: color for the circle
        """
        self.inp_r = h/15.
        self.stride = h/5
        self.inputs = []
        self.outputs = []
        self.noutlets = 0
        self.ninlets = 0
        Graph.__init__(self,parent,x+self.inp_r,y)
        self.objects[INLETS]=[]
        self.objects[OUTLETS]=[]
        self.objects[0].append(FancySquare(self,self.inp_r,0,w,h,col))
        self.objects[0].append(Label(self,self.inp_r,0,w,10,col=col,name=name))
        RectCollider.__init__(self,w+2*self.inp_r,h)
        if not ninlets == None:
            for i in xrange(ninlets):
                col_idx = random.randint(0,4)
                self.AddInlet(colors[col_idx])
        if not noutlets == None:
            for i in xrange(noutlets):
                col_idx = random.randint(0,4)
                self.AddOutlet(colors[col_idx])
        self.evstack.insert(0,evhandler(self))
    def Destroy(self):
        self.parent.objects[0].remove(self)
        for inlet in self.objects[INLETS]:
            inlet.ClearConnections()
        for outlet in self.objects[OUTLETS]:
            outlet.ClearConnections()
    def SetCol(self,col):
        self.objects[0][0].col = col
    def GetCol(self):
        return self.objects[0][0].col
    col = property(GetCol,SetCol)
    def SetHeight(self,h):
        self.objects[0][0].h = h
    def GetHeight(self):
        return self.objects[0][0].h
    h = property(GetHeight,SetHeight)
    col = property(GetCol,SetCol)

    def SetName(self,name):
        self.objects[0][1].name = name
    def GetName(self):
        return self.objects[0][1].name
    name = property(GetName,SetName)

    def GetNextNodes(self):
        nodes = []
        for outlet in self.objects[OUTLETS]:
            nodes += outlet.GetNextNodes()
        return nodes
    def GetPreviousNodes(self):
        nodes = []
        for inlet in self.objects[INLETS]:
            nodes += inlet.GetPreviousNodes()
        return nodes
    def GetNextNodesWithConnections(self):
        nodes = []
        for outlet in self.objects[OUTLETS]:
            for inlet,node in outlet.GetNextNodesWithConnections():
                nodes.append([inlet,outlet,node])
        return nodes
    def GetPreviousNodesWithConnections(self):
        nodes = []
        for inlet in self.objects[INLETS]:
            nodes += inlet.GetPreviousNodes()
            for outlet,node in outlet.GetPreviousNodesWithConnections():
                nodes.append([outlet,inlet,node])
        return nodes
    def IsRootNode(self):
        if len(self.GetPreviousNodes()):
            return False
        return True
    def AddInlet(self,col,con_type=NodeConnector):
        """
        Add an inlet to the node.
        @param col: color for the inlet
        @param con_type: class to create the connector from
        """
        i = self.ninlets
        self.objects[INLETS].append(con_type(self.parent,self,self.inp_r,(1+i)*self.stride,self.inp_r,col))
        self.ninlets+=1
        return self.objects[INLETS][-1]
    def GetOutlets(self):
        for idx in xrange(self.noutlets):
            yield self.GetOutlet(idx)
    def GetInlets(self):
        for idx in xrange(self.ninlets):
            yield self.GetInlet(idx)
    def GetInlet(self,idx):
        return self.objects[INLETS][idx]
    def GetOutlet(self,idx):
        return self.objects[OUTLETS][idx]
    def AddOutlet(self,col,con_type=NodeConnector):
        """
        Add an outlet to the node.
        @param col: color for the inlet
        @param con_type: class to create the connector from
        """
        i = self.noutlets
        self.objects[OUTLETS].append(con_type(self.parent,self,self.w-self.inp_r,(1+i)*self.stride,self.inp_r,col))
        self.noutlets+=1
        return self.objects[OUTLETS][-1]
    def NewNode(self,x,y):
        """
        Create a new node children of this one
        """
        obj_size = self.scale
        parent = self.parent
        root=self.Root()
        while True:
            obj_size *= parent.scale
            if parent==root:
                break
            parent = parent.parent

        obj_size = 30/obj_size
        self.objects[0].append(GraphNode(self,x-(obj_size/2),y-(obj_size/2),obj_size,obj_size))
        self.Redraw()


