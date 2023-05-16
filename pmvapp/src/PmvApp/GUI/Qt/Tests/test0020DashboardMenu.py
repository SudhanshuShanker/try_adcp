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
# $Header: /mnt/raid/services/cvs/PmvApp/GUI/Qt/Tests/test0020DashboardMenu.py,v 1.3.4.1 2017/07/13 20:47:44 annao Exp $
#
# $Id: test0020DashboardMenu.py,v 1.3.4.1 2017/07/13 20:47:44 annao Exp $
#
import unittest, sys
from .testBase import TestBase

from PySide import QtGui, QtCore

class DashboardSelectMenu(TestBase):

    def test_001_selectMenu(self):
        """test that when we read a molecule it appears in the dashboard
"""
        app = self.pmv
        gui = self.gui

        # read a molecule
        mols = app.readMolecules(["../../../Tests/Data/1crn.pdb",]) 

        # post menu on 1crn
        menu = gui.objTree.contextMenuEvent(None,
                                            item=mols[0][0]._treeItem())

        # find action name "Set as Selection"
        action = None
        for act in menu.actions():
            if act.text()=='Set as Selection':
                action = act
                break

        assert action is not None

        # invoke this action
        action.trigger()
        
        # check that we have a Current Selection in the Dashboard
        items = gui.objTree.findItems('Current Selection',
                                      QtCore.Qt.MatchExactly)
        assert len(items)==1
        assert items[0].text(0)=='Current Selection'
        assert hasattr(items[0], '_pmvObject')
        assert items[0]._pmvObject == app.curSelection

        # make sure Current Selection is active in GUI
        assert gui.activeSelection == app.curSelection
        
        # post menu on 1crn again
        menu = gui.objTree.contextMenuEvent(None,
                                            item=mols[0][0]._treeItem())

        # find action name "Deselect"
        action = None
        for act in menu.actions():
            if act.text()=='Deselect':
                action = act
                break

        assert action is not None

        # invoke this action
        action.trigger()

        # check that we the Current Selection is removed from the Dashboard
        items = gui.objTree.findItems('Current Selection',
                                      QtCore.Qt.MatchExactly)
        
        # we should not find the item
        assert len(items)==0

        # the gui should have no active selection
        assert gui.activeSelection is None

    def test_002_selectMenu(self):
        """test that"""

        app = self.pmv
        gui = self.gui

        # read a molecule
        mols = app.readMolecules(["../../../Tests/Data/1crn.pdb",]) 

        app.select("1crn::VAL15:CG1")

        # assert that Current selction is visible and active

        #simulate click on Current Selection
        previous = gui.objTree.currentItem()
        current = gui.objTree.findItems('Current Selection',
                                        QtCore.Qt.MatchExactly)
        gui.objTree.onSetCurrentItem(current[0], previous)

        assert gui.activeSelection == None
        assert gui.selectionCrosses.visible==0

        app.select("1crn::VAL15:CG2")
        current = gui.objTree.findItems('Current Selection',
                                        QtCore.Qt.MatchExactly)
        assert len(current)==1
        

class DashboardNameMenu(TestBase):
    """test that when we can rename objects in the dashboard"""

    def test_001_nameMolecule(self):
        """test rename one molecule"""
        app = self.pmv
        gui = self.gui

        # read a molecule
        mol = app.readMolecules(["../../../Tests/Data/1crn.pdb",])[0][0]

        # we actually do not trigger the action as the dialog is model
        gui.rename( ['foo'], [(mol, mol._treeItem())])

        # make sure the dashboard shows the name change
        items = gui.objTree.findItems('foo (1crn)',
                                      QtCore.Qt.MatchExactly)
        assert len(items)==1
        assert items[0] is mol._treeItem()

        # now create a selection containing 1crn
        # and verify that the item for 1crn in there is also renamed
        app.select("1crn::VAL15")
        # expand the current selection so that 1crn under the selection gets crated
        current = gui.objTree.findItems('Current Selection',
                                        QtCore.Qt.MatchExactly)[0]
        current.setExpanded(True)
        items = gui.objTree.findItems('foo (1crn)',
                         QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive)
        #for it in items:
        #    print it.text(0), it
        #self.app.exec_()
        assert len(items)==2
        

    def test_002_nameResidues(self):
        """test rename several residues"""
        app = self.pmv
        gui = self.gui

        # read a molecule
        #mols = app.readMolecules(["../../../Tests/Data/1crn.pdb",]) 
        mol = app.Mols[0]
        # expand 1crn
        print(mol._treeItem())
        mol._treeItem().setExpanded(True)
        # expand first chain
        list(mol.chains[0]._treeItems.values())[0].setExpanded(True)

        # select first 3 residues
        objItems = []
        for res in mol.chains[0].residues[:3]:
            item = list(res._treeItems.values())[0]
            objItems.append( (res, item) )
            item.setSelected(True)
            
        gui.rename( ['foo1','foo2','foo3'], objItems )

        for name, objIt in zip(['foo1','foo2','foo3'], objItems):
            res, item = objIt
            assert item.text(0).encode('ascii', 'ignore').startswith(name), "%s %s"%(item.text(0), name)
            
        gui.rename( ['bar','bar','bar'], objItems )

        for name, objIt in zip(['bar','bar','bar'], objItems):
            res, item = objIt
            assert item.text(0).encode('ascii', 'ignore').startswith(name), "%s %s"%(item.text(0), name)
            
        #self.app.exec_()
