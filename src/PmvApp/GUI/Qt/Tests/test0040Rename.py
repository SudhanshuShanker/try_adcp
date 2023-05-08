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
# $Header: /mnt/raid/services/cvs/PmvApp/GUI/Qt/Tests/test0040Rename.py,v 1.4.4.1 2017/07/13 20:47:44 annao Exp $
#
# $Id: test0040Rename.py,v 1.4.4.1 2017/07/13 20:47:44 annao Exp $
#
import unittest, sys
from .testBase import TestBase

from PySide import QtGui, QtCore

class TestRename0000(TestBase):

    def test_001_basicRename(self):
        """test some basic renaming operations"""

        app = self.pmv
        gui = self.gui

        # initially the app.activeSelection is app.curSelection
        assert app.activeSelection == app.curSelection
        # initially the gui.activeSelection is None because no selection is active in the GUI
        assert gui.activeSelection == None

        ##
        ## rename TreeNodes

        # Load 1crn
        mols = app.readMolecules(["../../../Tests/Data/1crn.pdb",])

        # rename the molecule using the handle to the molecule
        #import pdb; pdb.set_trace()
        app.rename(mols[0], 'foo')
        assert list(mols[0]._treeItems.keys())[0].text(0)=='foo (1crn)'

        # undo renaming molecule
        app.undo()
        assert list(mols[0]._treeItems.keys())[0].text(0)=='1crn'

        # check that passing a bad string will raise a value error
        self.assertRaises(ValueError, app.rename, *('abc', 'foo'))

        # rename the molecule using the object name
        app.rename('1crn', 'foo')
        assert list(mols[0]._treeItems.keys())[0].text(0)=='foo (1crn)'

        app.undo()
        assert list(mols[0]._treeItems.keys())[0].text(0)=='1crn'

        app.redo()
        assert list(mols[0]._treeItems.keys())[0].text(0)=='foo (1crn)'
        #self.app.exec_()
        # rename the first 3 residues before expanding the tree
        res3 = mols[0].chains.residues[:3]
        app.rename(res3, 'bar')
        # test that the names alias are set in the residues
        for res in res3:
            assert res.alias == 'bar'

        # expand 1crn to the residue level
        molItem = list(mols[0]._treeItems.keys())[0]
        molItem.setExpanded(True)
        mols[0].chains[0]._treeItems[molItem].setExpanded(True)
        for res in res3:
            assert res._treeItems[molItem].text(0) == 'bar (%s)'%res.name

        #print 'ABC', app.undo.cmdStack[-2:]
        # undo rename TreeNodes
        app.undo()
        for res in res3:
            assert res._treeItems[molItem].text(0) == res.name

        #print 'ABC1', app.undo.cmdStack[-2:]
        app.redo()
        for res in res3:
            assert res._treeItems[molItem].text(0) == 'bar (%s)'%res.name
        #self.app.exec_()
        # redo 
        app.redo()
        for res in res3:
            assert res._treeItems[molItem].text(0) == 'bar (%s)'%res.name
        app.rename(res3, 'bar')
        
        # rename 2 residues
        res6 = mols[0].chains.residues[3:5]
        #import pdb; pdb.set_trace()
        app.rename(res6, 'test')
        #self.app.exec_()
        
        for res in res6:
            assert res._treeItems[molItem].text(0) == 'test (%s)'%res.name
        
        # undo renaming TreeNodeSet
        app.undo()
        for i, res in enumerate(res6):
            assert res._treeItems[molItem].text(0) == res.name

        ##############################################################
        ##
        ## rename selection
        ##
        ##############################################################
            
        # select atoms in VAL15
        app.select("1crn::VAL15")
        
        # Verify that the dashboard has an entry called currentSelection
        items = gui.objTree.findItems('Current Selection', QtCore.Qt.MatchExactly)
        assert len(items)==1

        # name the selection
        app.rename(app.curSelection, 'firstSelection')

        # verify it worked
        items = gui.objTree.findItems('firstSelection', QtCore.Qt.MatchExactly)
        assert len(items)==1

        # check undo rename current selection
        #print 'UNDO is', app.undo.cmdStack[-1]
        app.undo()
        #self.app.exec_()
        assert app.activeSelection == app.curSelection
        assert len(app.namedSelections)==0
        assert gui.activeSelection == app.curSelection
        items = gui.objTree.findItems('Current Selection', QtCore.Qt.MatchExactly)
        assert len(items)==1

        app.redo()
        items = gui.objTree.findItems('firstSelection', QtCore.Qt.MatchExactly)
        assert len(items)==1

        app.rename('firstSelection', 'foo')
        items = gui.objTree.findItems('foo', QtCore.Qt.MatchExactly)
        assert len(items)==1
        assert app.activeSelection == app.namedSelections['foo']
        assert gui.activeSelection == app.namedSelections['foo']
        assert len(app.activeSelection.get())==7 # 7 atoms in VAL15

        # check undo rename named selection
        app.undo()
        #self.app.exec_()
        assert len(app.namedSelections)==1
        assert app.activeSelection == app.namedSelections['firstSelection']
        assert gui.activeSelection == app.namedSelections['firstSelection']
        items = gui.objTree.findItems('firstSelection', QtCore.Qt.MatchExactly)
        assert len(items)==1
        #self.app.exec_()

        # add to this selection should not create a new selection
        app.select("1crn::CYS16")
        items = gui.objTree.findItems('Current Selection', QtCore.Qt.MatchExactly)
        assert len(items)==0
        assert len(app.activeSelection.get())==13 # 7 atoms in VAL15 + 6 in CYS16

        ## create a second selection and make sure we can not rename
        ## it the same name
        # first simulate clicking on selection 'firstSelection' to turn it off
        gui.objTree.onSetCurrentItem(list(app.activeSelection._treeItems.keys())[0],
                                     gui.objTree.currentItem())
        assert gui.activeSelection == None
        assert app.activeSelection == app.curSelection

        ## now select something else
        #
        app.select("1crn::TYR29")

        # the selection should go into app.curSelection which should now be the active one
        items = gui.objTree.findItems('Current Selection', QtCore.Qt.MatchExactly)
        assert len(items)==1
        assert app.activeSelection == app.curSelection
        assert gui.activeSelection == app.curSelection
        #self.app.exec_()
        assert len(app.activeSelection.get())==12 # 12 atoms in TYR29

        ## make sure we can not rename a selection 'Current Selection'
        #
        sele = app.namedSelections['firstSelection']
        self.assertRaises(ValueError, app.rename, *(sele, 'Current Selection'))
        self.assertRaises(ValueError, app.rename, *(app.curSelection, 'firstSelection'))
        #self.app.exec_()

        ##
        ## rename groups
        grp1 = app.addGroup('Group1')
        app.rename(grp1, 'MyGroup1')

        # check that it worked
        items = gui.objTree.findItems('MyGroup1', QtCore.Qt.MatchExactly)
        assert len(items)==1
        
        # test undo
        app.undo()
        items = gui.objTree.findItems('Group1', QtCore.Qt.MatchExactly)
        assert len(items)==1
        
        # test redo 
        app.redo()
        #app.rename(grp1, 'MyGroup1')
        items = gui.objTree.findItems('MyGroup1', QtCore.Qt.MatchExactly)
        assert len(items)==1
        
        grp2 = app.addGroup('Group2')
        self.assertRaises(ValueError, app.rename, *(grp2, 'MyGroup1'))
        #self.app.exec_()
        
            
       
