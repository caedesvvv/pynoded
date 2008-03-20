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

from math import pi,atan2
from random import randint

import cairo
import gtk


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
		

#print "The secret word is " + word_chosen

def key_event(widget, event):
	print "key event"

def button_event(widget, event):
	print "button event"
	print event.x,event.y
	_, _, width, height = widget.allocation

	ctx.append_path(p)
	print ctx.in_fill(event.x,event.y)

def motion_event(widget, event):
	print "motion event"

def expose_event(widget, event):
    _, _, width, height = widget.allocation
    global p,ctx

    if width < height:
        size = width
    else:
        size = height

    pixmap = gtk.gdk.Pixmap (widget.window, width, height)
    ctx = pixmap.cairo_create()

    # set the background
    ctx.set_source_rgb(0.9,0.7,0.7)
    ctx.set_operator (cairo.OPERATOR_SOURCE)

    ctx.paint()

    ctx.set_source_rgb(0,0,0)
    ctx.set_line_width(7)
    ctx.rectangle(10,10,100,100)
    p=ctx.copy_path()
    ctx.stroke()

    
    Arrow((0,0,1),100,100,200.0,300.0).Draw(ctx)

    
    ctx.append_path(p)


    ctx.translate ((width - size) / 2, (height - size) / 2)
    ctx.scale(size / 150.0, size / 160.0)

    # draw on window
    gc = gtk.gdk.GC(widget.window)
    widget.window.draw_drawable(gc, pixmap, 0,0, 0,0, -1,-1)


win = gtk.Window()
win.add_events(gtk.gdk.KEY_PRESS_MASK |
             gtk.gdk.POINTER_MOTION_MASK |
             gtk.gdk.BUTTON_PRESS_MASK |
             gtk.gdk.SCROLL_MASK)

win.connect('destroy', gtk.main_quit)
win.connect('key_press_event', key_event)
win.connect('button_press_event', button_event)
win.connect('motion_notify_event', motion_event)
win.set_title('pygraph test')

drawingarea = gtk.DrawingArea()
win.add(drawingarea)
drawingarea.connect('expose_event', expose_event)
drawingarea.set_size_request(300,320)


win.show_all()
gtk.main()
