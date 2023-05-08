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

#
#################################################################
#       Author: Sowjanya Karnati
#################################################################
#
#Purpose:To update dependencies list
#
# $Id: test_dependencies.py,v 1.2.28.1 2017/07/31 04:37:02 annao Exp $
from mglutil.TestUtil.Tests.dependenciestest import DependencyTester
import unittest
d = DependencyTester()
result_expected =[]
class test_dep(unittest.TestCase):
    
    def test_dep_1(self):
        result = d.rundeptester('geomutils')    
        if result !=[]:
            print("\nThe Following Packages are not present in CRITICAL or NONCRITICAL DEPENDENCIES of geomutils :\n  %s" %result)
            self.assertEqual(result,result_expected) 
        else:
            self.assertEqual(result,result_expected)
    

if __name__ == '__main__':
    unittest.main()


