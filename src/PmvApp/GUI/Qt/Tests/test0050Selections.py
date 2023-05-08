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
# $Header: /mnt/raid/services/cvs/PmvApp/GUI/Qt/Tests/test0050Selections.py,v 1.1.4.1 2017/07/13 20:47:44 annao Exp $
#
# $Id: test0050Selections.py,v 1.1.4.1 2017/07/13 20:47:44 annao Exp $
#
import unittest, sys
from .testBase import TestBase

from PySide import QtGui, QtCore

class TestSelections0000(TestBase):

    def test_001_createSelection(self):
        """test dome basic selection behaviors"""

        app = self.pmv
        gui = self.gui

        # initially the app.activeSelection is app.curSelection
        assert app.activeSelection == app.curSelection
        # initially the gui.activeSelection is None because no selection is active in the GUI
        assert gui.activeSelection == None

        # Load 1crn
        mols = app.readMolecules(["../../../Tests/Data/1crn.pdb",])

        # select atoms in VAL15
        app.select("1crn::VAL15:")
        
        # Verify that the dashboard has an entry called currentSelection
        items = gui.objTree.findItems('Current Selection', QtCore.Qt.MatchExactly)
        assert len(items)==1

        # name the selection
        #app.namedSelections['Current Selectionsel.name] = sel
