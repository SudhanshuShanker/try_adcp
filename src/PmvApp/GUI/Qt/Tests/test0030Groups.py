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
# $Header: /mnt/raid/services/cvs/PmvApp/GUI/Qt/Tests/test0030Groups.py,v 1.6.4.1 2017/07/13 20:47:44 annao Exp $
#
# $Id: test0030Groups.py,v 1.6.4.1 2017/07/13 20:47:44 annao Exp $
#
import unittest, sys
from .testBase import TestBase

from PySide import QtGui, QtCore

class TestGroups(TestBase):

    def test_001_createGroupsThroughAPI(self):
        """test that when we create a group through PMV the group appear in the dashbaord
"""
        app = self.pmv
        gui = self.gui
        
        # create a empty group
        group1 = app.addGroup('Group1')

        # check that we have a Group1 item in the Dashboard
        items = gui.objTree.findItems('Group1',
                                      QtCore.Qt.MatchExactly)
        self.assertTrue(len(items)==1)
        self.assertTrue(len(app.groups)==1)
        self.assertTrue(app.groups[group1.name] == group1)
        self.assertTrue(group1._group is None)
        
        # create a group with a molecule
        group2 = app.addGroup('Group2')
        self.assertTrue(group2._group is None)
        mols = app.readMolecules(["../../../Tests/Data/1crn.pdb",])
        app.reparentObject(mols[0], group2)
        self.assertTrue(len(group2)==1)
        
        # check that we have a Group1 item in the Dashboard
        items2 = gui.objTree.findItems('Group2',
                                       QtCore.Qt.MatchExactly)
        self.assertTrue(len(items2)==1)
        self.assertTrue(len(app.groups)==2)
        self.assertTrue(app.groups[group2.name] == group2)

        # expand group 2
        items2[0].setExpanded(True)
        self.assertTrue(items2[0].childCount()==1)
        self.assertTrue(items2[0].child(0).text(0)=='1crn')

        ##
        ## move group 2 into group 1        
        app.reparentObject(group2, group1)
        self.assertTrue(gui.objTree.invisibleRootItem().childCount()==1)
        child = gui.objTree.invisibleRootItem().child(0)
        self.assertTrue(child.text(0)=='Group1')
        self.assertTrue(child.childCount()==1)
        grandChild = child.child(0)
        self.assertTrue(grandChild.text(0)=='Group2')
        self.assertTrue(grandChild.childCount()==1)
        grgrChild = grandChild.child(0)
        self.assertTrue(grgrChild.text(0)=='1crn')

        ##
        ## move Group2 out of Group1
        app.reparentObject(group2, None)
        self.assertTrue(gui.objTree.invisibleRootItem().childCount()==2)

        ##
        ## move Group2 out of Group1
        app.reparentObject(mols[0], None)
        self.assertTrue(gui.objTree.invisibleRootItem().childCount()==3)
        #self.app.exec_()
        ## delete group Group1
        app.deleteGroups([group1])
        self.assertTrue(gui.objTree.invisibleRootItem().childCount()==2)
        #self.app.exec_()

        # recreate group1 and move group2 and 1crn into group1
        group1 = app.addGroup('Group1')
        app.reparentObject(group2, group1)
        app.reparentObject(mols[0], group1)
        
        # delete group 1
        app.deleteGroups([group1])
        self.assertTrue(gui.objTree.invisibleRootItem().childCount()==0)

        # recreate group1 and reread the molecule
        #group1 = app.addGroup('Group1')
        #mols = app.readMolecules(["../../../Tests/Data/1crn.pdb",])
        #self.app.exec_()
        # recreate group1
        group1 = app.addGroup('Group1')
        # test addGroup() with optional "parentGroup" argument:
        # create group2 under group1

        items1 = gui.objTree.findItems('Group1',
                                       QtCore.Qt.MatchExactly)
        group2 = app.addGroup('Group2', group1)
        #self.app.exec_()
        self.assertTrue(items1[0].childCount() == 1)
        self.assertTrue(items1[0].child(0).text(0) == 'Group2')
        # add another group under group1 (use name for the parent):
        group3 = app.addGroup('Group3', 'Group1')
        self.assertTrue(items1[0].childCount() == 2)
        self.assertTrue(items1[0].child(1).text(0) == 'Group3')
        #self.app.exec_()
        # test the "group" option of readMolecules command
        mols = app.readMolecules(["../../../Tests/Data/1crn.pdb",], group=group1)
        self.assertTrue(items1[0].childCount() == 3)
        self.assertTrue(items1[0].child(2).text(0) == '1crn')
