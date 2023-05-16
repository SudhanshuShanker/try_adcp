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

import unittest
from .test_cube import TestBase
import sys
import numpy
import numpy.random as RandomArray
from opengltk.OpenGL import GL, GLUT

MY_LIST = 1
NUMDOTS = 500
NUMDOTS2 = 600
MAX_AGE = 13

class TestDots(TestBase):

    def setUp(self):
        from opengltk.OpenGL import GL, GLUT
        print("GL imported from: ", GL.__file__)
        #print "Hit any key to quit."
        self.x = RandomArray.random( NUMDOTS) * 2 - 1
        self.y = RandomArray.random( NUMDOTS) * 2 - 1

        self.age = RandomArray.randint( 0,MAX_AGE, (NUMDOTS,))
        move_length = 0.005  # 1.0 = screen width
        angle = 0		 # in radians
        delta_angle = 0.2  # in radians
        self.move_x = move_length * numpy.cos( angle)
        self.move_y = move_length * numpy.sin( angle)
        self.halted = 0
        
    def display(self):
	GL.glClearColor( 0.0, 0.0, 0.0, 0.0)
	GL.glClear( GL.GL_COLOR_BUFFER_BIT)
	GL.glColor3f( 1.0,1.0,0.0)
	self.x = self.x + self.move_x
	self.y = self.y + self.move_y
	self.age = self.age + 1
	which = numpy.greater( self.age, MAX_AGE)
	self.x = numpy.choose( which, (self.x, RandomArray.random( NUMDOTS)))
	selfy = numpy.choose( which, (self.y, RandomArray.random( NUMDOTS)))
	self.age = numpy.choose( which, (self.age, 0))
	self.x = numpy.choose( numpy.greater( self.x, 1.0), (self.x, self.x - 1.0)) 
	self.y = numpy.choose( numpy.greater( self.y, 1.0), (self.y, self.y - 1.0))
	x2 = RandomArray.random( NUMDOTS2)
	y2 = RandomArray.random( NUMDOTS2)
	v = numpy.concatenate(
		(numpy.transpose( numpy.array( [self.x, self.y])),
		 numpy.transpose( numpy.array( [self.x - 0.005, self.y + 0.005])),
		 numpy.transpose( numpy.array( [self.x + 0.005, self.y - 0.005])),
		 numpy.transpose( numpy.array( [x2, y2]))))
        #from opengltk.util import GLdouble
        #av = bufarray.readArray( v, GLdouble)
	#GL.glVertexPointer( 2, av)
        GL.glVertexPointer( 2, v)
	GL.glEnableClientState( GL.GL_VERTEX_ARRAY)
	#glplus.DrawArrays( GL.POINTS, len( av))
        from opengltk import  glplus
        glplus.DrawArrays( GL.GL_POINTS, len( v))
	#GL.glDisableClientState( GL.VERTEX_ARRAY)
	GL.glFlush()
	GLUT.glutSwapBuffers()


    def keyboard( self, key, x, y):
        print('--> keyboard( %s <%c>, %i, %i)' % ( key, chr( key), x, y))
        import sys
	sys.exit()

    def setup_viewport(self):
        GL.glMatrixMode( GL.GL_PROJECTION)
	GL.glLoadIdentity()
	GL.glOrtho( 0.0, 1.0, 0.0, 1.0, 0.0, 1.0)

    def reshape(self, w, h):
        GL.glViewport( 0, 0, w, h)
	self.setup_viewport()
    
    def test_dots(self):
        GLUT.glutInit( sys.argv)
        GLUT.glutInitDisplayMode( GLUT.GLUT_DOUBLE | GLUT.GLUT_RGB)
        GLUT.glutInitWindowSize( 300, 300)
        GLUT.glutCreateWindow( 'Dots')
        self.setup_viewport()
        GLUT.glutReshapeFunc( self.reshape)
        GLUT.glutDisplayFunc( self.display)
        GLUT.glutIdleFunc( None)
        GLUT.glutIdleFunc( self.display)
        GLUT.glutKeyboardFunc( self.keyboard)
        GLUT.glutTimerFunc(1000, self.exitloop, 0)
        GLUT.glutMainLoop()

    

if __name__ == '__main__':

    test_cases = ['TestDots']
    unittest.main(argv=([__name__, '-v'])+test_cases )
    
