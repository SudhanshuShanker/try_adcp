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

import gc

import unittest
from DejaVu2.Viewer import Viewer
from time import sleep
from tkinter import Tk, Frame, Toplevel
from DejaVu2.Spheres import Spheres


class memory_Tests(unittest.TestCase):
    """
tests for memory
    """
    #def setUp(self):
    #    self.root = Tk()
    #    self.root.withdraw()
#
#    def tearDown(self):
#        try:
#            self.root.destroy()
#        except:
#            pass


    def XXtest_creatingViewers100Time(self):
        """create a Viewer and destroy it 100 times"""

        #for i in range(100):
        #    vi = Viewer(verbose=0)
        #    vi.master.update()
        #    vi.Exit()
        #    gc.collect()
        self.assertEqual(1,1)



    def test_creatingViewers100TimeWithViewer(self):
        """create a Viewer and destroy it 100 times, when a Viewer already exists"""
        vi1 = Viewer(verbose=False)
        for i in range(10):
            vi = Viewer(verbose=0)
            vi.master.update()
            vi.Exit()
            gc.collect()
        vi1.Exit()
        gc.collect()
        self.assertEqual(1,1)



if __name__ == '__main__':
    test_cases = [
        'memory_Tests',
        ]
    
    unittest.main( argv=([__name__ ,] + test_cases) )
    #unittest.main()



