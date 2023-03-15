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
## (C) Copyrights Dr. Michel F. Sanner and TSRI 2016
##
################################################################################

from mglutil.math.rotax import interpolate3DTransform, rotax
from math import pi, sin, cos, sqrt
import numpy
import unittest

degtorad = pi/180.
                    
class Interpolate3DBaseTest(unittest.TestCase):
    def diff(self,res, expect):
        return res-expect < 1.0e-6  # close enough -> true
        
    def test_interpolate3D(self):
        mat1=rotax([0,0,0], [0,0,1],30.0*degtorad)
        mat2=rotax([0,0,0], [0,0,1],60.0*degtorad)
        mat3=rotax([0,0,0], [0,0,1],90.0*degtorad)
        # add translation (0,1,0) to mat2 
        mat2 = numpy.array([
               [ 0.5       ,  0.86602539,  0.        ,  0.        ],
               [-0.86602539,  0.5       ,  0.        ,  0.        ],
               [ 0.        ,  0.        ,  1.        ,  0.        ],
               [ 0.        ,  1.        ,  0.        ,  1.        ]],'f')
    
        matList=[mat1, mat2, mat3]
        indexList = [0.33333333, 0.66666666667, 1.0]
        data = [[0.,0.,0.,1.],[1.0, 0.0, 0.0,1.0],[2.,0.,0.,1.]]
        p=0.5
        M = interpolate3DTransform(matList, indexList, p)
        
        res=numpy.dot(data, M)[1]
        
        self.assertEqual( self.diff(res[0], 0.70710677 ),True)
        self.assertEqual(self.diff(res[1], 1.20710677 ),True) # 50% translation along Y axis
        self.assertEqual(self.diff(res[2], 0.0),True)
    
        p=1.5
        M = interpolate3DTransform(matList, indexList, p)
        res=numpy.dot(data, M)[1]
        self.assertEqual(self.diff(res[0], -0.70710677 ),True)
        self.assertEqual(self.diff(res[1],  0.70710677 ),True)
        self.assertEqual(self.diff(res[2],  0.0),True)


if __name__ == '__main__':
    unittest.main()
