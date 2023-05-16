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


"""
do not add any dependancy on this file
"""
import unittest
from opengltk.OpenGL import GL
from DejaVu2.Viewer import Viewer

class MaterialEditor_BaseTests(unittest.TestCase):


    def test_MaterialEditorDependancies(self):

        vi = Viewer()
        mated = vi.materialEditor
        mated.show()
        obj = vi.currentObject
        mated.setObject(obj, GL.GL_FRONT)
        mated.defineMaterial(obj.materials[GL.GL_FRONT].prop, GL.GL_FRONT)
        assert mated


if __name__ == '__main__':
    unittest.main()


