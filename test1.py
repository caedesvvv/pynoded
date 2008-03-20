#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2004 Kevin Worth
#
# Permission to use, copy, modify, distribute, and sell this software
# and its documentation for any purpose is hereby granted without fee,
# provided that the above copyright notice appear in all copies and
# that both that copyright notice and this permission notice appear in
# supporting documentation, and that the name of the Kevin Worth not
# be used in advertising or publicity pertaining to distribution of
# the software without specific, written prior permission. Kevin Worth
# California makes no representations about the suitability of this
# software for any purpose.  It is provided "as is" without express or
# implied warranty.
#
# KEVIN WORTH DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
# INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN
# NO EVENT SHALL KEVIN WORTH BE LIABLE FOR ANY SPECIAL, INDIRECT OR
# CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
# OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
# WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#
# Author: Kevin Worth <kevin@theworths.org>

from math import pi
from random import randint

import cairo
import gtk


#print "The secret word is " + word_chosen

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
        self.objects = []
    def key_event(self, widget, ev):
        print "key event"
    def button_press_event(self, widget, ev):
        print "button press event",ev.x,ev.y,ev.button
        self.objects.append(Square(ev.x-5,ev.y-5,10,10))
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

