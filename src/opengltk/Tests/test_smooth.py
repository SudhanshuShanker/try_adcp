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

import sys
from .test_cube import TestBase
from opengltk.OpenGL import GL, GLU, GLUT

class TestSmooth(TestBase):
   def triangle(self):
      GL.glBegin( GL.GL_TRIANGLES)
      try:
          GL.glColor3f( 1.0, 0.0, 0.0)
          GL.glVertex2f( 5.0, 5.0)
          GL.glColor3f( 0.0, 1.0, 0.0)
          GL.glVertex2f( 25.0, 5.0)
          GL.glColor3f( 0.0, 0.0, 1.0)
          GL.glVertex2f( 5.0, 25.0)
      finally:
          GL.glEnd()

   def display(self):
      GL.glClear(GL.GL_COLOR_BUFFER_BIT)
      self.triangle()
      GL.glFlush()


   def reshape(self, w, h):
      GL.glViewport( 0, 0, w, h)
      GL.glMatrixMode(GL.GL_PROJECTION)
      GL.glLoadIdentity()
      if(w <= h):
         GLU.gluOrtho2D( 0.0, 30.0, 0.0, 30.0 * h/w)
      else:
         GLU.gluOrtho2D( 0.0, 30.0 * w/h, 0.0, 30.0)
      GL.glMatrixMode( GL.GL_MODELVIEW)

   def setUp(self):
       from opengltk.OpenGL import GL,  GLU, GLUT
       print("GL imported from: ", GL.__file__)

   def test_Smooth(self):   
       self.doloop( 'Smooth', GL.GL_SMOOTH, self.display, self.reshape, self.keyboard)


if __name__ == '__main__':
   test_cases = ['TestSmooth']
   unittest.main(argv=([__name__, '-v'])+test_cases )

