#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from math import pi,atan2
import cairo
import gtk

class GraphObject(object):
    def __init__(self):
        pass
    def press(self,x,y):
        pass
    def release(self,x,y):
        pass
    def move(self,x,y):
        pass
    def Draw(self,ctx,scale):
        pass

class Arrow(object):
    def __init__(self,color,x0,y0,x1,y1):
        self.x0=x0
        self.x1=x1
        self.y0=y0
        self.y1=y1
        self.color=color
    def Draw(self,ctx):
        ctx.set_line_width(1)
        linewidth,_ = ctx.device_to_user_distance(1.,1.)
        ctx.set_line_width(linewidth)
        ctx.set_source_rgb(*self.color)
        ctx.move_to(self.x0,self.y0)
        ctx.line_to(self.x1,self.y1)
        angle=atan2((self.y1-self.y0),(self.x1-self.x0))
        ctx.rotate(angle)
        ctx.rel_line_to(-6,0)
        ctx.rel_line_to(0,3)
        ctx.rel_line_to(6,-3)
        ctx.rel_line_to(-6,-3)
        ctx.rel_line_to(0,3)
        ctx.fill_preserve()
        ctx.stroke()

class Square(object):
    def __init__(self,x,y,w,h,col=(0.1,0.1,0.1)):
        print "NEW SQUARE"
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.col = col
    def Draw(self,ctx):
        print "draw square"
        ctx.set_source_rgb(*self.col)
        linewidth,_ = ctx.device_to_user_distance(2.,2.)
        ctx.set_line_width(linewidth)
        ctx.rectangle(self.x,self.y,self.w,self.h)
        ctx.set_source_rgb( 1, 1, 1) 
        ctx.fill( )
        ctx.stroke()
        ctx.set_source_rgb( 0, 0, 0) 
        ctx.rectangle(self.x,self.y,self.w,self.h)
        ctx.stroke()

class CairoGraph(object):
    def __init__(self):
        self.objects = []
        self.scale = (1.0,1.0)
        self.pos = (0.0,0.0)
    def Create(self,x,y):
        obj_size = 10/self.scale[0]
        self.objects.append(Square(x-(obj_size/2),y-(obj_size/2),obj_size,obj_size))
        return True
    def Screen2Surface(self,x,y):
        x = float(x)
        y = float(y)
        return [(x/self.scale[0])-self.pos[0],(y/self.scale[1])-self.pos[1]]
    def DrawCairo(self,ctx):
        # set the background
        ctx.set_source_rgb(0.7,0.7,0.7)
        ctx.set_operator (cairo.OPERATOR_SOURCE)
        ctx.paint()
        # apply scale and position
        ctx.scale(*self.scale)
        ctx.translate (*self.pos)
        # draw all CairoObjects
        for obj in self.objects:
            obj.Draw(ctx)

    def Zoom(self,x,y,factor):
        pre_pos = self.Screen2Surface(x,y)
        self.scale = map(lambda s: s*factor,self.scale)
        post_pos = self.Screen2Surface(x,y)
        self.pos = map(lambda i: self.pos[i]+post_pos[i]-pre_pos[i],range(2))
    def MoveCenter(self,from_x,from_y,to_x,to_y):
        newpos = self.Screen2Surface(to_x,to_x)
        x = newpos[0]-from_x
        y = newpos[1]-from_y
        self.pos = [self.pos[0]+x,self.pos[1]+y]
        self.movepos = self.Screen2Surface(to_x,to_x)

class GtkBackend(gtk.DrawingArea,CairoGraph):
    def __init__(self):
        super(GtkBackend,self).__init__()
        CairoGraph.__init__(self)
        self.add_events(gtk.gdk.KEY_PRESS_MASK |
                        gtk.gdk.POINTER_MOTION_MASK |
                        gtk.gdk.BUTTON_PRESS_MASK |
                        gtk.gdk.BUTTON_RELEASE_MASK |
                        gtk.gdk.SCROLL_MASK)
        self.connect('key_press_event', self.key_press_event)
        self.connect('button_press_event', self.button_press_event)
        self.connect('button_release_event', self.button_release_event)
        self.connect('motion_notify_event', self.motion_event)
        self.connect('expose_event', self.expose_event)
        self.connect('scroll_event', self.scroll_event)
        self.keyp_cbs = {"+" : lambda ev : Zoom(ev.x,ev.y,1/0.99),
                         "-" : lambda ev : Zoom(ev.x,ev.y,0.99)}
        self.keyr_cbs = {}
        self.mousep_cbs = [self.Create,None,self.StartMove]
        self.mouser_cbs = [None,None,self.EndMove]

    def key_press_event(self, widget, ev):
        print "KEY EVENT"
        keyp_cbs[ev.string](ev.x,ev.y)

    def key_release_event(self,widget, ev):
        keyr_cbs[ev.string](ev.x,ev.y)

    def StartMove(self,x,y):
        self.movepos = [x,y]
        self.connect('motion_notify_event', self.move_screen)

    def EndMove(self,x,y):
        self.disconnect_by_func(self.move_screen)
    def move_screen(self,widget,ev):
        self.movepos = self.MoveCenter(self.movepos[0],
                                        self.movepos[1],ev.x,ev.y)
        self.Redraw()
    def Redraw(self):
        self.queue_draw_area(0,0,1000,1000)

    def Zoom(self,x,y,factor):
        CairoGraph.Zoom(self,x,y,factor)
        self.Redraw()

    def scroll_event(self, widget, ev):
        if ev.direction == gtk.gdk.SCROLL_DOWN:
            self.Zoom(ev.x,ev.y,0.99)
        else:
            self.Zoom(ev.x,ev.y,1/0.99)

    def button_press_event(self, widget, ev):
        x,y = self.Screen2Surface(ev.x,ev.y)
        callback = self.mousep_cbs[ev.button-1]
        if callback and callback(x,y):
            self.Redraw()
    def button_release_event(self, widget, ev):
        print "button release event",ev.x,ev.y,ev.button
        x,y = self.Screen2Surface(ev.x,ev.y)
        callback = self.mouser_cbs[ev.button-1]
        if callback and callback(x,y):
            self.Redraw()

    def motion_event(self, widget, ev):
        pass

    def expose_event(self, widget, event):
        _, _, width, height = widget.allocation

        if width < height:
            size = width
        else:
            size = height

        pixmap = gtk.gdk.Pixmap (widget.window, width, height)
        ctx = pixmap.cairo_create()

        self.DrawCairo(ctx)

        # draw on window
        gc = gtk.gdk.GC(widget.window)
        widget.window.draw_drawable(gc, pixmap, 0,0, 0,0, -1,-1)

def run(Widget,title="test app"):
    window = gtk.Window()
    window.set_title(title)
    window.connect("delete-event", gtk.main_quit)
    widget = Widget()
    widget.show()
    window.add(widget)
    window.present()
    gtk.main()

run(GtkBackend,"pygraph test")
