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

import unittest, sys
from AppFramework.App import AppFramework

class CreateApp(unittest.TestCase):

    def test_001_sanityCheck(self):
        """
        tests that the App is created
        """
        app = AppFramework('test')
        app.exit()
        assert sys.getrefcount(app)==2

    def test_001_checkMemoryuse(self):
        import resource, gc
        # create an App to use up some memory
        app = AppFramework('test')
        app.exit()
        gc.collect()
        
        # check how much mem Python is using
        memInKb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss  
        # create the app again, If the memory use by previous app has
        # been released the python process should not grow more
        app = AppFramework('test')
        app.exit()
        gc.collect()
        newMemUse = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        self.assertTrue(memInKb == newMemUse, "Memory leak %d -> %d : %d"%(memInKb, newMemUse, newMemUse-memInKb))
       

if __name__ == '__main__':
    import os, testBase
    os.chdir(os.path.split(testBase.__file__)[0])
    unittest.main()
