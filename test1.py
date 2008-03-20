#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import cairo
import gtk

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
        ctx.set_line_width(6)
        ctx.rectangle(self.x,self.y,self.w,self.h)
        ctx.stroke()

class GtkBackend(gtk.DrawingArea):
    def __init__(self):
        super(GtkBackend,self).__init__()
        self.add_events(gtk.gdk.KEY_PRESS_MASK |
                     gtk.gdk.POINTER_MOTION_MASK |
                     gtk.gdk.BUTTON_PRESS_MASK |
                     gtk.gdk.BUTTON_RELEASE_MASK |
                     gtk.gdk.SCROLL_MASK)
        self.connect('key_press_event', self.key_event)
        self.connect('button_press_event', self.button_press_event)
        self.connect('button_release_event', self.button_release_event)
        self.connect('motion_notify_event', self.motion_event)
        self.connect('expose_event', self.expose_event)
        self.connect('scroll_event', self.scroll_event)
        self.objects = []
        self.scale = (1.0,1.0)
        self.press_cbs = [self.Create,self.StartScale]
        self.release_cbs = [None,None]
    def key_event(self, widget, ev):
        print "key event"
    def Create(self,x,y):
        print "create"
        self.objects.append(Square(x-5,y-5,10,10))
        return True
    def StartScale(self,x,y):
        self.scale_start = (x,y)
        self.connect('motion_notify_event', self.ScaleChange)
    def ScaleChange(self, widget, ev):
        scale_x = ev.x
        scale_y = ev.y
    def EndScale(self,x,y):
        pass
    def scroll_event(self, widget, ev):
        print "scroll event",ev.x,ev.y,dir(ev),ev.direction
        if ev.direction == gtk.gdk.SCROLL_DOWN:
            factor = -0.01
        else:
            factor = 0.01
        self.scale = map(lambda s: s+factor,self.scale)
        self.queue_draw_area(0,0,1000,1000)
    def button_press_event(self, widget, ev):
        print "button press event",ev.x,ev.y,ev.button
        x = (ev.x)/self.scale[0]
        y = (ev.y)/self.scale[1]
        callback = self.press_cbs[ev.button-1]
        if callback and callback(x,y):
            self.queue_draw_area(0,0,1000,1000)
    def button_release_event(self, widget, ev):
        print "button release event",ev.x,ev.y,ev.button

    def motion_event(self, widget, ev):
        print "motion event",ev.x,ev.y
    def expose_event(self, widget, event):
        _, _, width, height = widget.allocation

        if width < height:
            size = width
        else:
            size = height

        pixmap = gtk.gdk.Pixmap (widget.window, width, height)
        ctx = pixmap.cairo_create()
        
        # set the background
        ctx.set_source_rgb(0.7,0.7,0.7)
        ctx.set_operator (cairo.OPERATOR_SOURCE)
        ctx.paint()

        #ctx.translate ((width - size) / 2, (height - size) / 2)
        ctx.scale(*self.scale)

        #ctx.translate ((width - size) / 2, (height - size) / 2)
        #ctx.scale(size / 150.0, size / 160.0)
        for obj in self.objects:
            obj.Draw(ctx)

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

