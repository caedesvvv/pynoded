from graph import *
from evhandler import *
from evhandlers import *
from shapes import GraphNode
import gtk
import cairo

class MainGraph(gtk.DrawingArea,Graph):
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        Graph.__init__(self)
        self.evstack=EvStack()
        self.evstack.stack.append(DefaultEvH(self))
        self.evstack.stack.append(PropagateEvH(self))
        self.pos=(0,0)
        self.scale=1
        self.objects[1]=[]

    def GetPointer(self):
        return self.Screen2Surface(*self.get_pointer())

    def Draw(self,ctx):
        # set the background
        ctx.set_source_rgb(0.7,0.7,0.7)
        ctx.set_operator (cairo.OPERATOR_SOURCE)
        ctx.paint()
        # apply scale and position
        ctx.scale(self.scale,self.scale)
        ctx.translate (*self.pos)
        Graph.Draw(self,ctx)

    def Screen2Surface(self,x,y):
        x = float(x)
        y = float(y)
        return [(x/self.scale)-self.pos[0],(y/self.scale)-self.pos[1]]

    def Zoom(self,x,y,factor):
        pre_pos = self.Screen2Surface(x,y)
        self.scale *=factor
        post_pos = self.Screen2Surface(x,y)
        self.pos = map(lambda i: self.pos[i]+post_pos[i]-pre_pos[i],range(2))
        self.queue_draw()
 
    def NewNode(self,dest=None):
        if not dest:
            dest = self
        x,y=self.GetPointer()
        obj_size = 30/self.scale
        dest.objects[0].append(GraphNode(self,x-(obj_size/2),y-(obj_size/2),obj_size,obj_size))
        self.evstack.expose()


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
        self.maingraph.NewNode()
        return True

    def mousepress_right(self):
        x,y=self.maingraph.get_pointer()
        self.maingraph.evstack.stack.append(ScrollEvH(self.maingraph,x,y))
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
        self.initpos=maingraph.pos
        self.initmx=initmx
        self.initmy=initmy

    def mouse_motion(self,x,y):
        dx,dy=float(x-self.initmx),float(y-self.initmy)
        self.maingraph.pos=(self.maingraph.pos[0]+dx/self.maingraph.scale,self.maingraph.pos[1]+dy/self.maingraph.scale)
        self.initpos=self.maingraph.pos
        self.initmx,self.initmy=x,y
        self.maingraph.queue_draw()
        return True

    def mouserelease_right(self):
        self.maingraph.evstack.stack.remove(self)
        return True

class PropagateEvH(EvHandler):
    def __init__(self,maingraph):
        self.maingraph=maingraph

    def __getattr__(self,name):
        x,y=self.maingraph.GetPointer()
        return lambda *args: self.maingraph.Propagate(x,y,name,*args)
