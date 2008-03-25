#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from pygraph.maingraph import *
import gtk

def run(widget,evh,title="test app"):
    window = gtk.Window()
    def key_press_event(widget,ev):
        if ev.string=="+":
            evh.keypress_plus()
        elif ev.string=="-":
            evh.keypress_minus()
        elif ev.string=="c":
            evh.keypress_c()
    def key_release_event(widget,ev):
        pass
    def button_press_event(widget,ev):
        if ev.type!=gtk.gdk.BUTTON_PRESS:
            return
        if ev.button==1:
            evh.mousepress_left()
        elif ev.button==2:
            evh.mousepress_middle()
        elif ev.button==3:
            evh.mousepress_right()
    def button_release_event(widget,ev):
        if ev.button==1:
            evh.mouserelease_left()
        elif ev.button==2:
            evh.mouserelease_middle()
        elif ev.button==3:
            evh.mouserelease_right()
    def motion_notify_event(widget,ev):
        evh.mouse_motion(ev.x,ev.y)
    def expose_event(widget,ev):
        evh.expose()
    def scroll_event(widget,ev):
        if ev.direction==gtk.gdk.SCROLL_UP:
            evh.scroll_up()
        elif ev.direction==gtk.gdk.SCROLL_DOWN:
            evh.scroll_down()

            
    window.connect("delete-event", gtk.main_quit)
    window.connect('key_press_event', key_press_event)
    window.connect('key_release_event',key_release_event)
    widget.add_events(gtk.gdk.KEY_PRESS_MASK |
                        gtk.gdk.KEY_RELEASE_MASK |
                        gtk.gdk.POINTER_MOTION_MASK |
                        gtk.gdk.BUTTON_PRESS_MASK |
                        gtk.gdk.BUTTON_RELEASE_MASK |
                        gtk.gdk.SCROLL_MASK)
    widget.connect('button_press_event', button_press_event)
    widget.connect('button_release_event', button_release_event)
    widget.connect('motion_notify_event', motion_notify_event)
    widget.connect('expose_event', expose_event)
    widget.connect('scroll_event', scroll_event)
     
    window.set_title(title)
    widget.show()
    window.add(widget)
    window.present()
    gtk.main()

mg=MainGraph()
run(mg.widget,mg.evstack,"pygraph test")
