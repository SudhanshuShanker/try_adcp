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

#
#
# $Id: test_tester.py,v 1.3.30.1 2017/07/26 22:35:40 annao Exp $
#

#########################################################################
#
# Date: July 2003  Author: Sophie Coon
#
#       sophiec@scripps.edu
#
# Copyright: TSRI, Sophie Coon.
#
#########################################################################

import unittest, os


class TestSuiteTest(unittest.TestCase):
    pass

class TestLoaderTest(unittest.TestCase):
    """
    TestCase class implementing methods to test Tester functionalities
    """
    def setUp(self):
        from mglutil.TestUtil.tester import TestLoader
        self.tl = TestLoader()

    def tearDown(self):
        self.tl = None

    def test_loadTestsFromTestCase1(self):
        from .Data.test_displayCommands import DisplayLinesTest
        suite = self.tl.loadTestsFromTestCase(DisplayLinesTest)
        self.assertTrue(isinstance(suite, self.tl.suiteClass))
        self.assertEqual(len(suite._tests), 5)

    
##     def test_loadTestsFromFunctions(self):
##         from Data import test_secondarystructure
##         mod = test_secondarystructure
##         import types
##         funcs = []
##         for name in dir(test_secondarystructure):
##             if name[:4]=='test':
##                 f = getattr(mod,name)
##                 if type(f) is types.FunctionType:
##                     funcs.append(f)
                    
##         setUp = getattr(mod,"startMoleculeViewer")
##         tearDown = getattr(mod,"quitMoleculeViewer")
##         path,testSuite = self.tl.loadTestsFromFunctions(funcs,setUp=setUp,
##                                                    tearDown=tearDown)
##         self.failUnless(isinstance(testSuite, self.tl.suiteClass))
##         self.assertEqual(len(testSuite._tests),19)
        
##         path, testSuite = self.tl.loadTestsFromFunctions(funcs[0])
##         self.failUnless(isinstance(testSuite, self.tl.suiteClass))
##         self.assertEqual(len(testSuite._tests),1)

    def test_loadTestsFromModule_1(self):
        from .Data import test_secondarystructure
        mod = test_secondarystructure
        path,testSuite = self.tl.loadTestsFromModule(mod)
        self.assertTrue(isinstance(testSuite, self.tl.suiteClass))
        self.assertEqual(len(testSuite._tests), 19)

    def test_loadTestsFromModule_2(self):
        from .Data import test_displayCommands
        mod = test_displayCommands
        path,testSuite = self.tl.loadTestsFromModule(mod)
        
    def test_loadTestsFromName_1(self):
        name = 'mglutil.TestUtil.Tests.test_tester'
        path,ts = self.tl.loadTestsFromName(name)
        self.assertTrue(isinstance(ts, self.tl.suiteClass))
        self.assertTrue(len(ts._tests)!=0)
        
    def test_loadTestsFromName_2(self):
        name = 'mglutil.TestUtil'
        path,ts = self.tl.loadTestsFromName(name)
        self.assertTrue(isinstance(ts, self.tl.suiteClass))
        self.assertTrue(len(ts._tests)!=0)

    def test_loadTestsFromPackage_1(self):
        from mglutil import TestUtil
        print(os.path.abspath(TestUtil.__path__[0]))
        r = self.tl.loadTestsFromPackage(TestUtil)
        print(r)
        #self.failUnless(isinstance(ts, self.tl.suiteClass))
        #self.failUnless(len(ts._tests)!=0)

        
class TesterTest(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
