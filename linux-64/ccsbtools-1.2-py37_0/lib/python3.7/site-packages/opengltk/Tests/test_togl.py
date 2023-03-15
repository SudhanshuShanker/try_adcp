################################################################################
##
## This library is free software; you can redistribute it and/or
## modify it under the terms of the GNU Lesser General Public
## License as published by the Free Software Foundation; either
## version 2.1 of the License, or (at your option) any later version.
## 
## This library is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## Lesser General Public License for more details.
## 
## You should have received a copy of the GNU Lesser General Public
## License along with this library; if not, write to the Free Software
## Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
##
## Copyright (c) MGL TSRI 2016
##
################################################################################

import tkinter
from opengltk.OpenGL import GL
import unittest
import os
import numpy

class OGLTkWidget(tkinter.Widget, tkinter.Misc):

    def __init__(self, master, cnf={}, expand=1, **kw):

        if 'width' not in kw: kw['width']=150
        if 'height' not in kw: kw['height']=150
        if 'double' not in kw: kw['double']=1

        from opengltk.OpenGL import Tk
        from os import path
        ToglPath = path.dirname(path.abspath(Tk.__file__))
        # get TCL interpreter auto_path variable
        tclpath = master.tk.globalgetvar('auto_path')

        # ToglPath not already in there, add it
        from string import split
        if ToglPath not in tclpath:
            tclpath = (ToglPath,) + tclpath
            master.tk.globalsetvar('auto_path', tclpath )
        #load Togl extension into TCL interpreter
        master.tk.call('package', 'require', 'Togl', '1.7')

        # create an Tk-OpenGL widget
        tkinter.Widget.__init__(self, master, 'togl', cnf, kw)

        self.bind('<Expose>', self.tkExpose)
        self.bind('<Enter>', self.Enter_cb)
        self.bind('<Configure>', self.Configure)

        self.pack(side='left')


    def initProjection(self):
        GL.glMatrixMode (GL.GL_PROJECTION)
        GL.glLoadIdentity ()
        GL.glOrtho(-10., 10., -10., 10., -10., 10.)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GL.glTranslatef(0, 0, 10.0)


    def tkExpose(self, *dummy):
        self.tk.call(self._w, 'makecurrent')
        self.initProjection()
        self.tkRedraw()


    def Activate(self):
        self.tk.call(self._w, 'makecurrent')


    def Enter_cb(self, event):
        """Call back function trigger when the mouse enters the camera"""
        self.tk.call(self._w, 'makecurrent')


    def Configure(self, *dummy):
        """Cause the opengl widget to redraw itself."""
        #print 'Configure 0'
        width = self.winfo_width()
        height = self.winfo_height()
        GL.glViewport(0, 0, width, height)


    def tkRedraw(self, *dummy):
        #if not self.winfo_ismapped(): return
        self.update_idletasks()
        self.tk.call(self._w, 'makecurrent')
        self.initProjection()
        GL.glPushMatrix()
        self.redraw()
        GL.glFlush()
        GL.glPopMatrix()
        self.tk.call(self._w, 'swapbuffers')


    def setupLightModel(self):
        # this method has to be called explicitly by the derived classes if
        # a default lighting model is wanted
        GL.glLight(GL.GL_LIGHT0, GL.GL_AMBIENT,  [.5, .5, .5, 1.0])
        GL.glLight(GL.GL_LIGHT0, GL.GL_DIFFUSE,  [.5, .5, .5, 1.0])
        GL.glLight(GL.GL_LIGHT0, GL.GL_SPECULAR, [.5, .5, .5, 1.0])
        GL.glLight(GL.GL_LIGHT0, GL.GL_POSITION, [1.0, 1.0, 1.0, 0.0]);   

        GL.glLight(GL.GL_LIGHT1, GL.GL_AMBIENT,  [.5, .5, .5, 1.0])
        GL.glLight(GL.GL_LIGHT1, GL.GL_DIFFUSE,  [.5, .5, .5, 1.0])
        GL.glLight(GL.GL_LIGHT1, GL.GL_SPECULAR, [.5, .5, .5, 1.0])
        GL.glLight(GL.GL_LIGHT1, GL.GL_POSITION, [-1.0, 1.0, 1.0, 0.0]);   

        GL.glLightModel(GL.GL_LIGHT_MODEL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        GL.glEnable(GL.GL_LIGHTING)
        GL.glEnable(GL.GL_LIGHT0)
        GL.glEnable(GL.GL_LIGHT1)

    def redraw(self):
        GL.glColor3f( 0., 0., 0. )
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)


class TestTogl(unittest.TestCase):

    def test_0030( self):
        # creates an OpenGL context inside a togl widget
        # can be used to test any opengl function
        import tkinter
        root = tkinter.Tk()
        vi = OGLTkWidget(root)
        root.after(500, root.quit )
        root.mainloop()
        root.destroy()


    def test_0031(self ):
        # example we test glMultMatrixf
        import tkinter
        root = tkinter.Tk()
        vi = OGLTkWidget(root)
        id = numpy.array([1.,0.,0.,0.,
                            0.,1.,0.,0.,
                            0.,0.,1.,0.,
                            0.,0.,0.,1.], "d")
        from opengltk.extent import _gllib as gllib
        #GL.glMultMatrixf(id)
        try:
            gllib.cvar.checkArgumentsInCWrapper = 0
            GL.glMultMatrixf(id)
            # calling with bad argument
            gllib.cvar.checkArgumentsInCWrapper = 1
            id = numpy.identity(4).astype('d')
            try:
                GL.glMultMatrixf(id)
                raise RuntimeError('failed to catch type error in wrapper')
            except TypeError:
                print('Type Error caught succefully in wrapper')
        except ImportError:
            pass

        root.after(1000, root.quit )
        root.mainloop()
        root.destroy()
        
    def test_0032(self ):
        import tkinter
        root = tkinter.Tk()
        vi = OGLTkWidget(root)
        GL.glBegin( GL.GL_TRIANGLES)
        GL.glColor3f( 1.0, 0.0, 0.0)
        GL.glVertex2f( 5.0, 5.0)
        GL.glColor3f( 0.0, 1.0, 0.0)
        GL.glVertex2f( 25.0, 5.0)
        GL.glColor3f( 0.0, 0.0, 1.0)
        GL.glVertex2f( 5.0, 25.0)
        GL.glEnd()
        root.after(500, root.quit )
        root.mainloop()
        root.destroy()

if __name__ == '__main__':
    test_cases = ['TestTogl']
    unittest.main(argv=([__name__, '-v'])+test_cases )
