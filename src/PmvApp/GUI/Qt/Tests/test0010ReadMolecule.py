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

#############################################################################
#
# Author: Michel F. SANNER
#
# Copyright: M. Sanner TSRI 2014
#
#############################################################################

#
# $Header: /mnt/raid/services/cvs/PmvApp/GUI/Qt/Tests/test0010ReadMolecule.py,v 1.2.4.1 2017/07/13 20:47:44 annao Exp $
#
# $Id: test0010ReadMolecule.py,v 1.2.4.1 2017/07/13 20:47:44 annao Exp $
#
import unittest, sys
from .testBase import TestBase

from PySide import QtGui, QtCore

class ReadMolecule(TestBase):

    def test_001_readMolecule(self):
        """test that when we read a molecule the it appears in the dashboard
"""
        app = self.pmv
        gui = self.gui
        # read a molecule
        mols = app.readMolecules(["../../../Tests/Data/1crn.pdb",]) 

        # find the child names u'1crn' in the tree
        items = gui.objTree.findItems('1crn', QtCore.Qt.MatchExactly)
        #self.app.exec_()
        #import pdb
        #pdb.set_trace()
        assert len(items)==1
        assert items[0].text(0)=='1crn'
        assert hasattr(items[0], '_pmvObject')
        assert items[0]._pmvObject == app.Mols[0]
        assert app.Mols[0] == mols[0][0]
        assert id(mols[0][0]._treeItem()) == id(items[0])
        #print len(items), items[0].text(0)
        
if __name__ == '__main__':
    import os, testBase
    os.chdir(os.path.split(testBase.__file__)[0])
    unittest.main()
