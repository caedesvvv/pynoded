from graph import *
from evhandler import *
from evhandlers import *
from shapes import GraphNode
import gtk
import cairo

class MainGraph(gtk.DrawingArea,Graph):
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        Graph.__init__(self,None,0,0)
        self.evstack.insert(0,DefaultEvH(self))
        self.objects[1]=[]

    def GetPointer(self):
        return self.ToLocal(*self.get_pointer())

    def Draw(self,ctx):
        # set the background
        ctx.set_source_rgb(0.7,0.7,0.7)
        ctx.set_operator (cairo.OPERATOR_SOURCE)
        ctx.paint()
        Graph.Draw(self,ctx)

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
        self.queue_draw()

    def ToGlobal(self,x,y):
        return (x,y)

class DefaultEvH(EvHandler):
    def __init__(self,maingraph):
        self.maingraph=maingraph

    def scroll_up(self):
        x,y=self.maingraph.get_pointer()
        self.maingraph.Zoom(x,y,1/0.99)
        
    def keypress_plus(self):
        self.maingraph.Zoom(self.maingraph.allocation.width/2,self.maingraph.allocation.height/2,1/0.99)
        return True

    def scroll_down(self):
        x,y=self.maingraph.get_pointer()
        self.maingraph.Zoom(x,y,0.99)

    def keypress_minus(self):
        self.maingraph.Zoom(self.maingraph.allocation.width/2,self.maingraph.allocation.height/2,0.99)
        return True

    def keypress_c(self):
        self.maingraph.NewNode(*self.maingraph.GetPointer())
        return True

    def mousepress_right(self):
        x,y=self.maingraph.get_pointer()
        self.maingraph.evstack.append(ScrollEvH(self.maingraph,x,y))
        return True

    def mouse_motion(self,x,y):
        return True

    def expose(self):
        _,_,width,height=self.maingraph.allocation
        pixmap = gtk.gdk.Pixmap (self.maingraph.window, width, height)
        ctx = pixmap.cairo_create()

        self.maingraph.Draw(ctx)

        # draw on window
        gc = gtk.gdk.GC(self.maingraph.window)
        self.maingraph.window.draw_drawable(gc, pixmap, 0,0, 0,0, -1,-1)
        return True

class ScrollEvH(EvHandler):
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

    def mouserelease_right(self):
        self.maingraph.evstack.remove(self)
        return True
