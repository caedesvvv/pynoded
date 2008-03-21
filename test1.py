#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from math import pi,atan2
import cairo
import gtk

from pygraph.shapes import GraphNode

class CairoGraph(object):
    def __init__(self):
        self.objects = []
        self.scale = (1.0,1.0)
        self.pos = (0.0,0.0)
    def Create(self,x,y):
        obj_size = 30/self.scale[0]
        self.objects.append(GraphNode(x-(obj_size/2),y-(obj_size/2),obj_size,obj_size))
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
        newpos = self.Screen2Surface(to_x,to_y)
        x = newpos[0]-from_x
        y = newpos[1]-from_y
        self.pos = [self.pos[0]+x,self.pos[1]+y]
        return self.Screen2Surface(to_x,to_y)

class GtkBackend(gtk.DrawingArea,CairoGraph):
    def __init__(self):
        super(GtkBackend,self).__init__()
        CairoGraph.__init__(self)
        self.add_events(gtk.gdk.KEY_PRESS_MASK |
                        gtk.gdk.KEY_RELEASE_MASK |
                        gtk.gdk.POINTER_MOTION_MASK |
                        gtk.gdk.BUTTON_PRESS_MASK |
                        gtk.gdk.BUTTON_RELEASE_MASK |
                        gtk.gdk.SCROLL_MASK)
        self.connect('button_press_event', self.button_press_event)
        self.connect('button_release_event', self.button_release_event)
        self.connect('motion_notify_event', self.motion_event)
        self.connect('expose_event', self.expose_event)
        self.connect('scroll_event', self.scroll_event)
	self.keyp_cbs = {"+" : self.Key_plus,
                         "-" : self.Key_minus}
	self.keyr_cbs = {}
        self.mousep_cbs = [self.Create,self.Select,self.StartMove]
        self.mouser_cbs = [None,self.EndSelect,self.EndMove]
        self.motion_function=None

    def key_press_event(self, widget, ev):
        ev.string in self.keyp_cbs and self.keyp_cbs[ev.string]()
    def key_release_event(self,widget, ev):
        ev.string in self.keyr_cbs and self.keyr_cbs[ev.string]()

    def StartMove(self,x,y):
        self.movepos = [x,y]
        self.motion_function=self.move_screen

    def EndMove(self,x,y):
        self.motion_function=None

    def move_screen(self,widget,ev):
        self.movepos = self.MoveCenter(self.movepos[0],
                                        self.movepos[1],ev.x,ev.y)
        self.Redraw()
    def Redraw(self):
        self.queue_draw()

    def Zoom(self,x,y,factor):
        CairoGraph.Zoom(self,x,y,factor)
        self.Redraw()

    def scroll_event(self, widget, ev):
        if ev.direction == gtk.gdk.SCROLL_DOWN:
            self.Zoom(ev.x,ev.y,0.99)
        else:
            self.Zoom(ev.x,ev.y,1/0.99)

    def button_press_event(self, widget, ev):
        print "BPE"
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
        self.motion_function and self.motion_function(widget,ev)

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

    def Key_plus(self):
        self.Zoom(self.allocation.width/2,self.allocation.height/2,1/0.99)

    def Key_minus(self):
        self.Zoom(self.allocation.width/2,self.allocation.height/2,0.99)

    def Select(self,x,y):
        for i in range(len(self.objects)-1,-1,-1):
            o=self.objects[i]
            if o.Test(x,y):
                self.objects.pop(i)
                self.objects.append(o)
                def mfunct(widget,event):
                    o.Move(*self.Screen2Surface(event.x,event.y))
                    widget.queue_draw()
                self.motion_function=mfunct
                break
        return True

    def EndSelect(self,x,y):
        self.motion_function=None


def run(Widget,title="test app"):
    window = gtk.Window()
    window.set_title(title)
    window.connect("delete-event", gtk.main_quit)
    widget = Widget()
    window.connect('key_press_event', widget.key_press_event)
    window.connect('key_release_event', widget.key_release_event)
     
    widget.show()
    window.add(widget)
    window.present()
    gtk.main()

run(GtkBackend,"pygraph test")
