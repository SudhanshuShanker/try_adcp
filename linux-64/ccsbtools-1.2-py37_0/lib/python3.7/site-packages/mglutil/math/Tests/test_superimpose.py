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

from mglutil.regression import testplus
from mglutil.math.rotax import interpolate3DTransform, rotax
#from math import pi, sin, cos, sqrt
#degtorad = pi/180.
                    
def diff(res, expect):
    return res-expect < 1.0e-6  # close enough -> true




def test_superimpose():
    from mglutil.math.rigidFit import RigidfitBodyAligner
    rigidfitAligner = RigidfitBodyAligner()
    refCoords=[[0,0,0] , [1,0,0], [0,1,0], [0,0,1]]
    mobCoords=[[10,0,0] , [11,0,0], [10,1,0], [10,0,1]]
    rigidfitAligner.setRefCoords(refCoords)                
    rigidfitAligner.rigidFit(mobCoords)
    rmsd=rigidfitAligner.rmsdAfterSuperimposition(mobCoords)
    assert diff(rmsd, 0.0 )
