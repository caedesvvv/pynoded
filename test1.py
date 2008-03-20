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
    def Draw(self,ctx,size):
        print "draw square"
        ctx.set_source_rgb(*self.col)
        ctx.set_line_width(2./size)
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
        self.press_cbs = [self.Create,None,self.StartMove]
        self.release_cbs = [None,None,self.EndMove]
        self.pos = (0.0,0.0)
    def key_event(self, widget, ev):
        print "key event"
    def StartMove(self,x,y):
        self.movepos = [x,y]
        self.connect('motion_notify_event', self.move_screen)
    def EndMove(self,x,y):
        self.disconnect_by_func(self.move_screen)
    def move_screen(self,widget,ev):
        newpos = self.Screen2Surface(ev.x,ev.y)
        x = newpos[0]-self.movepos[0]
        y = newpos[1]-self.movepos[1]
        self.pos = [self.pos[0]+x,self.pos[1]+y]
        self.movepos = self.Screen2Surface(ev.x,ev.y)
        self.queue_draw_area(0,0,1000,1000)
    def Create(self,x,y):
        obj_size = 10/self.scale[0]
        self.objects.append(Square(x-(obj_size/2),y-(obj_size/2),obj_size,obj_size))
        return True
    def Redraw(self):
        self.queue_draw_area(0,0,1000,1000)
    def Screen2Surface(self,x,y):
        x = float(x)
        y = float(y)
        return [(x/self.scale[0])-self.pos[0],(y/self.scale[1])-self.pos[1]]
    def scroll_event(self, widget, ev):
        pre_pos = self.Screen2Surface(ev.x,ev.y)
        if ev.direction == gtk.gdk.SCROLL_DOWN:
            factor = 0.99
        else:
            factor = 1.01
        self.scale = map(lambda s: s*factor,self.scale)
        post_pos = self.Screen2Surface(ev.x,ev.y)
        self.pos = map(lambda i: self.pos[i]+post_pos[i]-pre_pos[i],range(2))
        self.Redraw()
    def button_press_event(self, widget, ev):
        x,y = self.Screen2Surface(ev.x,ev.y)
        callback = self.press_cbs[ev.button-1]
        if callback and callback(x,y):
            self.Redraw()
    def button_release_event(self, widget, ev):
        print "button release event",ev.x,ev.y,ev.button
        x,y = self.Screen2Surface(ev.x,ev.y)
        callback = self.release_cbs[ev.button-1]
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
        
        # set the background
        ctx.set_source_rgb(0.7,0.7,0.7)
        ctx.set_operator (cairo.OPERATOR_SOURCE)
        ctx.paint()

        ctx.scale(*self.scale)
        ctx.translate (*self.pos)

        #ctx.translate ((width - size) / 2, (height - size) / 2)
        #ctx.scale(size / 150.0, size / 160.0)
        for obj in self.objects:
            obj.Draw(ctx,self.scale[1])

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
