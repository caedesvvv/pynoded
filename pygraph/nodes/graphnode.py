"""
Graph nodes
"""
from pygraph.evhandlers import MoveEvH
from pygraph.graph import *
from pygraph.shapes import Square,Label,FancySquare
from pygraph.nodes.connection import NodeConnector
import random

colors = [(1,0,0),(0,1,0),(1,1,1),(1,0,1),(0,0,1)]

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
    def __init__(self,parent,x,y,w,h,name="",ninlets=None,noutlets=None,evhandler=GraphNodeEvH,col=(0.1,0.1,0.1)):
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
        self.name = name
        self.noutlets = 0
        self.ninlets = 0
        RectCollider.__init__(self,w+2*self.inp_r,h)
        Graph.__init__(self,parent,x+self.inp_r,y)
        self.objects[1]=[]
        self.objects[0].append(FancySquare(self,self.inp_r,0,w,h,col))
        self.objects[0].append(Label(self,self.inp_r,0,w,10,col=col,name=name))
        if not ninlets == None:
            for i in xrange(ninlets):
                col_idx = random.randint(0,4)
                self.AddInlet(colors[col_idx])
        if not noutlets == None:
            for i in xrange(noutlets):
                col_idx = random.randint(0,4)
                self.AddOutlet(colors[col_idx])
        self.evstack.insert(0,evhandler(self))

    def AddInlet(self,col,con_type=NodeConnector):
        """
        Add an inlet to the node.
        @param col: color for the inlet
        @param con_type: class to create the connector from
        """
        i = self.ninlets
        self.objects[1].append(con_type(self.parent,self,self.inp_r,(1+i)*self.stride,self.inp_r,col))
        self.ninlets+=1
    def AddOutlet(self,col,con_type=NodeConnector):
        """
        Add an outlet to the node.
        @param col: color for the inlet
        @param con_type: class to create the connector from
        """
        i = self.noutlets
        self.objects[1].append(con_type(self.parent,self,self.w-self.inp_r,(1+i)*self.stride,self.inp_r,col))
        self.noutlets+=1
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


