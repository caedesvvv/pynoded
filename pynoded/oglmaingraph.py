"""
OpenGL graph backend
"""

from graph import *
from evh.graph import GraphEvH
from nodes import GraphNode
import cairo
import Blender
import b2cs
import OpenGL
import OpenGL.GL
try:
    import numpy
except:
    pass

class OpenglMainGraph(MainGraph):
    def __init__(self,evh=GraphEvH):
        self.parent=self
        MainGraph.__init__(self,None,0,0)
        self.evstack.insert(0,evh(self))
        self.Width = 0
        self.Height = 0

    def GetRawPointer(self):
        point = b2cs.gui.get_corrected_mousepos(Blender.Window.GetAreaID())
        point[1] = self.Height-point[1]
        return point

    def SetSize(self,w,h):
        if  w == self.Width and h == self.Height:
            return
        self.Width = w
        self.Height = h
        self.CreateContext()
        self.ctx.rectangle(0,0,w/2,h/2)
        self.ctx.clip()

    def Draw(self):
        # set the background
        ctx = self.ctx
        ctx.set_source_rgb(0.7,0.7,0.7)
        ctx.set_operator (cairo.OPERATOR_SOURCE)
        ctx.paint()
        Graph.Draw(self,ctx)

    def CreateContext(self):
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                           int(self.Width),
                                           int(self.Height))
        ctx = cairo.Context(self.surface)
        self.ctx = ctx
        return ctx

    def Blit(self):
        surface = self.ctx.get_target()
        s_h = surface.get_height()
        s_w = surface.get_width()
        try:
             a = numpy.frombuffer(surface.get_data(), numpy.uint8)
        except:
             a = str(surface.get_data())
        #a.shape = (s_h,s_w, 4)
        #a = a[::-1,:,:]
        #s = a.tostring()
        try:
            OpenGL.GL.glRasterPos2f(0.0,float(s_h)-2.0)
            # 2 pixels offset sucks, but otherwise ogl doesnt draw at all...
            # must investigate further into matter (XXX).
        except:
            return # sometimes opengl doesnt want to do this.. :P
        OpenGL.GL.glPixelZoom(1.0,-1.0)
        OpenGL.GL.glDrawPixels (int(s_w),
                      int(s_h),
                      #Blender.BGL.GL_BGRA, Blender.BGL.GL_UNSIGNED_BYTE,
                      0x80E1, 0x1401,
                      a)
        OpenGL.GL.glPixelZoom(1.0,1.0)

    def NewNode(self,x,y):
        obj_size = 30/self.scale
        bb = self.CenteredBB(x,y,obj_size)
        obj = GraphNode(self,*bb)
        self.AddNode(obj)

    def Redraw(self):
        wID = Blender.Window.GetAreaID()
        Blender.Window.QAdd(wID,Blender.Draw.REDRAW,0,1)

    RawPointer = property(GetRawPointer)
