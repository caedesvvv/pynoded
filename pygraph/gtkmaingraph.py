"""
Gtk Graph Backend
"""
from graph import *
#from evhandler import *
#from evhandlers import *
from evh.graph import *
from nodes import GraphNode
import gtk
import cairo

class GtkMainGraph(Graph):
    """
    MainGraph for gtk contexts
    Use as follows:
      mg = GtkMainGraph()
      run(mg.widget, mg.evstack, "pygraph test")
    """
    def __init__(self,evh=GraphEvH):
        self.widget=gtk.DrawingArea()
        self.parent=self
        Graph.__init__(self,None,0,0)
        self.evstack.insert(0,evh(self))
        self.objects[1]=[]
        self.ctx = None
        self._prevw = 0
        self._prevh = 0

    def GetPointer(self):
        return self.ToLocal(*self.widget.get_pointer())

    def GetRawPointer(self):
        return self.widget.get_pointer()

    def Draw(self):
        # set the background
        #self.ctx.rectangle()
        self.ctx.set_source_rgb(0.7,0.7,0.7)
        self.ctx.set_operator (cairo.OPERATOR_SOURCE)
        self.ctx.paint()
        Graph.Draw(self,self.ctx)

    def CreateContext(self):
        if self.Width == self._prevw and self.Height == self._prevh:
            return
        self.pixmap = gtk.gdk.Pixmap (self.widget.window, 
                                 self.Width, self.Height)
        self._prevw = self.Width
        self._prevh = self.Height
        ctx = self.pixmap.cairo_create()
        self.ctx = ctx
        return ctx

    def Blit(self):
        gc = gtk.gdk.GC(self.widget.window)
        self.widget.window.draw_drawable(gc, self.pixmap, 0,0, 0,0, -1,-1)

    def Zoom(self,x,y,factor):
        pre_x,pre_y = self.ToLocal(x,y)
        self.scale *=factor
        post_x,post_y = self.ToLocal(x,y)
        self.x,self.y = (self.x+post_x-pre_x,self.y+post_y-pre_y)
        self.Redraw()
 
    def NewNode(self,x,y):
        obj_size = 30/self.scale
        self.objects[0].append(GraphNode(self,x-(obj_size/2),y-(obj_size/2),obj_size,obj_size))
        self.Redraw()

    def Redraw(self):
        self.widget.queue_draw()

    def ToGlobal(self,x,y):
        return (x,y)

    def Root(self):
        return self
    def Test(self,x,y):
        return True
    def GetWidth(self):
        return self.widget.allocation.width
    def GetHeight(self):
        return self.widget.allocation.height
    Width = property(GetWidth)
    Height = property(GetHeight)
    RawPointer = property(GetRawPointer)
    Pointer = property(GetPointer)

