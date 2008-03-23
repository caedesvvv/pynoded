from gobject import *
from shapes import GraphNode
import gtk
import cairo

class MainMap(GObjMap,gtk.DrawingArea):
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        GObjMap.__init__(self)
        self.evstack=EvStack()
        self.evstack.stack.append(PropagateEvH(self))
        self.evstack.stack.append(DefaultEvH(self))
        self.pos=(0,0)
        self.scale=1
        

    def Draw(self,ctx):
        # set the background
        ctx.set_source_rgb(0.7,0.7,0.7)
        ctx.set_operator (cairo.OPERATOR_SOURCE)
        ctx.paint()
        # apply scale and position
        ctx.scale(self.scale,self.scale)
        ctx.translate (*self.pos)
        GObjMap.Draw(self,ctx)

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
 
    def NewNode(self):
        x,y=self.Screen2Surface(*self.get_pointer())
        obj_size = 30/self.scale
        self.objects.append(GraphNode(self,x-(obj_size/2),y-(obj_size/2),obj_size,obj_size))
        self.evstack.expose()


class DefaultEvH(EvHandler):
    def __init__(self,mainmap):
        self.mainmap=mainmap

    def scroll_up(self):
        x,y=self.mainmap.get_pointer()
        self.mainmap.Zoom(x,y,1/0.99)
        
    def keypress_plus(self):
        self.mainmap.Zoom(self.mainmap.allocation.width/2,self.mainmap.allocation.height/2,1/0.99)
        return True

    def scroll_down(self):
        x,y=self.mainmap.get_pointer()
        self.mainmap.Zoom(x,y,0.99)

    def keypress_minus(self):
        self.mainmap.Zoom(self.mainmap.allocation.width/2,self.mainmap.allocation.height/2,0.99)
        return True

    def mousepress_left(self):
        self.mainmap.NewNode()
        return True

    def mousepress_right(self):
        x,y=self.mainmap.get_pointer()
        self.mainmap.evstack.stack.append(ScrollEvH(self.mainmap,x,y))
        return True

    def mouse_motion(self,x,y):
        return True

    def expose(self):
        _,_,width,height=self.mainmap.allocation
        pixmap = gtk.gdk.Pixmap (self.mainmap.window, width, height)
        ctx = pixmap.cairo_create()

        self.mainmap.Draw(ctx)

        # draw on window
        gc = gtk.gdk.GC(self.mainmap.window)
        self.mainmap.window.draw_drawable(gc, pixmap, 0,0, 0,0, -1,-1)
        return True

class PropagateEvH(EvHandler):
    def __init__(self,mainmap):
        self.mainmap=mainmap

    def __getattr__(self,name):
        x,y=self.mainmap.get_pointer()
        o=self.mainmap.ObjectAt(x,y)
        return lambda *args: o and getattr(o,name,False) and getattr(o,name)(*args)

class ScrollEvH(EvHandler):
    def __init__(self,mainmap,initmx,initmy):
        self.mainmap=mainmap
        self.initpos=mainmap.pos
        self.initmx=initmx
        self.initmy=initmy

    def mouse_motion(self,x,y):
        dx,dy=float(x-self.initmx),float(y-self.initmy)
        self.mainmap.pos=(self.mainmap.pos[0]+dx/self.mainmap.scale,self.mainmap.pos[1]+dy/self.mainmap.scale)
        self.initpos=self.mainmap.pos
        self.initmx,self.initmy=x,y
        self.mainmap.queue_draw()
        return True

    def mouserelease_right(self):
        self.mainmap.evstack.stack.remove(self)
        return True
