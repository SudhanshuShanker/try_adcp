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
# $Header: /mnt/raid/services/cvs/PmvApp/GUI/Qt/Tests/test0060Surface.py,v 1.2.4.1 2017/07/13 20:47:44 annao Exp $
#
# $Id: test0060Surface.py,v 1.2.4.1 2017/07/13 20:47:44 annao Exp $
#
import unittest, sys
from .testBase import TestBase

from PySide import QtGui, QtCore
from PySide.QtGui import QKeyEvent
from PySide.QtCore import Qt, QEvent

class MyEvent(QKeyEvent):
    def __init__(self, type, key, text, modifier=Qt.NoModifier):
        # Fix This; not sure how the key value corresponds to event.text()
        QKeyEvent.__init__(self, type, key, modifier)
        self._text = text

    def text(self):
        return self._text
    

class DashboardSurface(TestBase):

    def test_001_surface(self):
        """test tha we can use 'Add Representation -> surface' menu for computing/displaying MSMS"""
        app = self.pmv
        gui = self.gui

        # read a molecule
        mol = app.readMolecules(["../../../Tests/Data/1crn.pdb",])[0] 
        app.displayLines(mol)
        # post menu on 1crn
        menu = gui.objTree.contextMenuEvent(None,
                                            item=list(mol._treeItems.keys())[0])
        action = [act for act in menu.actions() if act.text()=="Add Representation"]
        self.assertTrue(len(action))
        rmenu = action[0].menu()
        raction = [act for act in rmenu.actions() if act.text()=="surface"]
        self.assertTrue(len(raction))
        # this is "surface" menu entry, trigger the execution of displayMSMS
        # commnad for 1crn
        raction[0].trigger()
        gc = mol.geomContainer
        surfName = 'surface-%s'%mol.name
        self.assertTrue(surfName in gc.geoms)
        surf = gc.geoms[surfName]
        nverts = 6044
        nfaces = 12084
        self.assertTrue(len(surf.vertexSet) == nverts)
        self.assertTrue(len(surf.faceSet) == nfaces)
        # check that the 1crn menu contains surfName (surface-1crn)
        menu = gui.objTree.contextMenuEvent(None,
                                            item=list(mol._treeItems.keys())[0])
        surfmenu = [act for act in menu.actions() if act.text()==surfName]
        self.assertTrue (len(surfmenu) == 1)

        # undisplay surface for 1crn
        remove = [act for act in surfmenu[0].menu().actions() if act.text()=="Remove"]
        self.assertTrue (len(remove) == 1)
        remove[0].trigger()
        surf = gc.geoms[surfName]
        self.assertTrue(surf.visible == 0)
        # check that the menu for 1crn does not have surface-1crn entry
        # after the surface was removed
        menu = gui.objTree.contextMenuEvent(None,
                                            item=list(mol._treeItems.keys())[0])
        surfmenu = [act for act in menu.actions() if act.text()==surfName]
        self.assertTrue (len(surfmenu) == 0)

        # make a selection:
        app.select(mol.chains[0].residues[:2])
        selatoms = app.activeSelection.atoms.name
        # simulate click on "Current Selection -> Add Representation -> surface"
        csmenu = gui.objTree.contextMenuEvent(None,
                                            item=list(app.curSelection._treeItems.keys())[0])
        
        action = [act for act in csmenu.actions() if act.text()=="Add Representation"]
        self.assertTrue(len(action))
        rmenu = action[0].menu()
        surfmenu = [act for act in rmenu.actions() if act.text()=="surface"]
        self.assertTrue(len(surfmenu) == 1)

        surfmenu[0].trigger()
        gc = mol.geomContainer
        surf = gc.geoms[surfName]
        nverts = 6044
        #print "faces:", len(surf.faceSet)
        nfaces = 518
        self.assertTrue(len(surf.vertexSet) == nverts)
        self.assertTrue(len(surf.faceSet) == nfaces)
        # check that the menu for 1crn has surface-1crn entry
        # since current selection is part of the molecule
        menu = gui.objTree.contextMenuEvent(None,
                                            item=list(mol._treeItems.keys())[0])
        surfmenu = [act for act in menu.actions() if act.text()==surfName]
        self.assertTrue (len(surfmenu) == 1)
        
        # undisplay surface for current selection:
        csmenu = gui.objTree.contextMenuEvent(None,
                                            item=list(app.curSelection._treeItems.keys())[0])
        surfmenu = [act for act in csmenu.actions() if act.text()==surfName]
        remove = [act for act in surfmenu[0].menu().actions() if act.text()=="Remove"]
        self.assertTrue (len(remove) == 1)
        remove[0].trigger()
        surf = gc.geoms[surfName]
        self.assertTrue(surf.visible == 0)
        
        # check that the menu for 1crn and the menu for current selection
        # do not have surface-1crn entry after the surface was removed:
        # 1crn menu
        menu = gui.objTree.contextMenuEvent(None,
                                            item=list(mol._treeItems.keys())[0])
        surfmenu = [act for act in menu.actions() if act.text()==surfName]
        self.assertTrue (len(surfmenu) == 0)
        # currentSelection menu
        csmenu = gui.objTree.contextMenuEvent(None,
                                            item=list(app.curSelection._treeItems.keys())[0])
        surfmenu = [act for act in csmenu.actions() if act.text()==surfName]
        self.assertTrue (len(surfmenu) == 0)

        items = gui.objTree.findItems('Current Selection', QtCore.Qt.MatchExactly)
        self.assertTrue(len(items)==1)
        # rename current selection 
        app.rename(app.curSelection, 'mySelection')
        
        # turn off named selection and add some atoms to currentSelection(current selection will contain some of the named selection) 
        gui.objTree.onSetCurrentItem(list(app.activeSelection._treeItems.keys())[0],
                                     gui.objTree.currentItem())
        app.select(mol.chains[0].residues[1:4])
        items = gui.objTree.findItems('Current Selection', QtCore.Qt.MatchExactly)
        assert len(items)==1
        # compute surface for the named selection
        sel = app.namedSelections['mySelection']
        selmenu = gui.objTree.contextMenuEvent(None,
                                   item=list(sel._treeItems.keys())[0])
        action = [act for act in selmenu.actions() if act.text()=="Add Representation"]
        self.assertTrue(len(action))
        rmenu = action[0].menu()
        surfmenu = [act for act in rmenu.actions() if act.text()=="surface"]
        self.assertTrue(len(surfmenu) == 1)
        surfmenu[0].trigger()
        gc = mol.geomContainer
        surfName = "surface-mySelection"
        surf = gc.geoms[surfName]
        #print "verts:", len(surf.vertexSet)
        #print "faces:", len(surf.faceSet)
        newfaces = 996
        newverts = 500
        self.assertTrue(len(surf.vertexSet) == newverts)
        self.assertTrue(len(surf.faceSet) == newfaces)
        msmsatoms = mol.geomContainer.msmsAtoms[surfName].name
        self.assertEqual(selatoms, msmsatoms)
        
        # remove surface for "mySelection"
        selmenu = gui.objTree.contextMenuEvent(None,
                                   item=list(sel._treeItems.keys())[0])
        surfmenu = [act for act in selmenu.actions() if act.text()==surfName]
        remove = [act for act in surfmenu[0].menu().actions() if act.text()=="Remove"]
        self.assertTrue (len(remove) == 1)
        remove[0].trigger()
        self.assertTrue(surf.visible == 0)
        
        # add some atoms to my selection
        gui.objTree.onSetCurrentItem(list(sel._treeItems.keys())[0],
                                     gui.objTree.currentItem())
        app.select(mol.chains[0].residues[2])

        # display surface for "mySelection" again, check that
        #the number of verts and faces is different
        selmenu = gui.objTree.contextMenuEvent(None,
                                   item=list(sel._treeItems.keys())[0])
        action = [act for act in selmenu.actions() if act.text()=="Add Representation"]
        rmenu = action[0].menu()
        surfmenu = [act for act in rmenu.actions() if act.text()=="surface"]
        surfmenu[0].trigger()
        surf = gc.geoms[surfName]
        #print "verts:", len(surf.vertexSet)
        #print "faces:", len(surf.faceSet)
        newfaces = 1358
        newverts = 681
        self.assertTrue(len(surf.vertexSet) == newverts)
        self.assertTrue(len(surf.faceSet) == newfaces)
        
        # check  that the menus for molecule and currentSelection contain
        # "surface-mySelection" entry
        # 1crn menu

        menu = gui.objTree.contextMenuEvent(None,
                                            item=list(mol._treeItems.keys())[0])
        surfmenu = [act for act in menu.actions() if act.text()==surfName]
        self.assertTrue (len(surfmenu) == 1)
        # currentSelection menu
        csmenu = gui.objTree.contextMenuEvent(None,
                                            item=list(app.curSelection._treeItems.keys())[0])
        surfmenu = [act for act in csmenu.actions() if act.text()==surfName]
        self.assertTrue (len(surfmenu) == 1)
        
        # remove surface in current Selection
        remove = [act for act in surfmenu[0].menu().actions() if act.text()=="Remove"]
        self.assertTrue (len(remove) == 1)
        remove[0].trigger()
        surf = gc.geoms[surfName]
        #print "verts:", len(surf.vertexSet)
        #print "faces:", len(surf.faceSet)
        newverts = 681
        newfaces = 546
        self.assertTrue(len(surf.vertexSet) == newverts)
        self.assertTrue(len(surf.faceSet) == newfaces)

        #self.app.exec_()


    def test_002_surfaceKeyPress(self):
        """ test key press event to toggle display/undisplay MSMS"""
        app = self.pmv
        gui = self.gui

        # read a molecule
        mol = app.readMolecules(["../../../Tests/Data/protease.pdb",])[0]
        #select it in the dashboard
        gui.objTree.setCurrentItem(list(mol._treeItems.keys())[0])
        app.displayLines(mol)
        surfName = 'surface-%s'%mol.name
        gc = mol.geomContainer

        # simulate "m" key press:
        # not sure how QKeyEvent works (how the key value corresponds to event.text())
        event = MyEvent(QEvent.KeyPress, 77, "m")
        #import pdb; pdb.set_trace()
        gui.objTree.keyPressEvent(event)
        self.assertTrue(surfName in gc.geoms)
        surf = gc.geoms[surfName]
        #print "verts:", len(surf.vertexSet)
        #print "faces:", len(surf.faceSet)
        nverts = 22698
        nfaces = 45396
        self.assertTrue(len(surf.vertexSet) == nverts)
        self.assertTrue(len(surf.faceSet) == nfaces)
        self.assertTrue(surf.visible == 1)

        # "press" m again
        gui.objTree.keyPressEvent(event)
        surf = gc.geoms[surfName]
        self.assertTrue(surf.visible == 0)
