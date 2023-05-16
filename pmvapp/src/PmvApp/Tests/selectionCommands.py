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
# Author: Michel F. SANNER, Anna Omelchenko
#
# Copyright: M. Sanner TSRI 2014
#
#############################################################################

#
# $Header: /mnt/raid/services/cvs/PmvApp/Tests/selectionCommands.py,v 1.3.4.1 2017/07/13 20:50:45 annao Exp $
#
# $Id: selectionCommands.py,v 1.3.4.1 2017/07/13 20:50:45 annao Exp $
#
import unittest
from . import testBase
from .testBase import TestBase
from mglutil.errors import MGLException

#from PmvApp.Pmv import MolApp
#app = MolApp()
#from AppFramework.notOptionalCommands import UndoCommand
#app.addCommand(UndoCommand(), 'undo')


class TestGuiApp:
    def __init__(self, app):
        self.app = app
        from PmvApp.selectionCmds import selectionFeedbackEvent, SelectionEvent
        #self.app.eventHandler.registerListener(selectionFeedbackEvent, self.handleSelectionFeedbackEvent)
        self.app.eventHandler.registerListener(SelectionEvent, self.handleSelectionFeedbackEvent)
        self.selectionEventCalled = False

    def clearEventFlag(self):
        self.selectionEventCalled = False

    def handleSelectionFeedbackEvent(self, event, **kw):
        #print "handleSelectionFeedbackEvent"
        self.selectionEventCalled = True
        

class TestSelect(TestBase):

    def setUp(self):
        if not self.app.getMolFromName('ind'):
            #print "SetUp: reading molecule Data/ind.pdb"
            self.app.readMolecule("Data/ind.pdb")
        if not hasattr(self.app, 'undo'):
            from AppFramework.notOptionalCommands import UndoCommand,\
                 RedoCommand
            self.app.addCommand(UndoCommand(), 'undo')
            self.app.addCommand(RedoCommand(), 'redo')
        if not hasattr(self.app, "GUI"):
            self.app.GUI = TestGuiApp(self.app)


    def test_001_loadCommand(self):
        """test that we can load file commands to Application"""
        #from PmvApp.Pmv import MolApp
        #app = MolApp()
        app = self.app
        cmds = ['select', 'deselect', 'clearSelection', 'directSelect']
        app.lazyLoad('selectionCmds', commands=cmds,
                     package='PmvApp')
        for cmd in cmds:
            self.assertTrue( hasattr(app, cmd))
            self.assertTrue(cmd in app.commands)
            app.commands[cmd].loadCommand()
            self.assertTrue(cmd in app.commands)


    def test_002_select(self):
        # select the molecule
        mol = self.app.Mols[0]
        
        sel = self.app.select("ind")  # CHECK THIS: it used to return a molecule
        # - now it return an atom set (??????)
        #self.assertEqual(sel[0], mol)
        # test "negate" (deselect molecule)
        self.app.GUI.clearEventFlag()
        sel = self.app.select(mol, negate=True)
        self.assertTrue(len(sel) == 0)
        self.assertTrue(self.app.GUI.selectionEventCalled == True)
        from Molkit2.molecule import Atom
        # the following fails (????)
        # test "klass"
        #sel = self.app.select(mol, klass=Atom)
        # sel is still a protein (?)
        #self.assertEqual(sel == mol.allAtoms)
        # test nodes
        sel1 = self.app.select("ind:I:IND201:C19,H30")
        self.assertEqual(len(sel1), 2)
        self.assertEqual(sel1[0].name, 'C19')
        self.assertEqual(sel1[1].name, 'H30')

        sel2 = self.app.select(mol.allAtoms[:10])
        self.assertEqual(len(self.app.activeSelection.get()), 12)
        # test "negate"
        sel3 = self.app.select("ind:I:IND201:C19,H30", negate=True)
        self.assertEqual(self.app.activeSelection.get(), mol.allAtoms[:10] )
        # test deselect()
        self.app.GUI.clearEventFlag()
        self.app.deselect(mol)
        self.assertTrue(self.app.GUI.selectionEventCalled == True)
        self.assertEqual(len(self.app.activeSelection.get()), 0)
        # test undo
        self.app.GUI.clearEventFlag()
        self.app.undo()
        self.assertEqual(self.app.activeSelection.get(), mol.allAtoms[:10])
        self.assertTrue(self.app.GUI.selectionEventCalled == True)
        # test "only"
        # add 5 atoms to the current selection
        self.app.select( mol.allAtoms[10:15])
        self.assertEqual(self.app.activeSelection.get(), mol.allAtoms[:15])
        # select only 5 atoms from  the current selection
        self.app.select( mol.allAtoms[10:15], only=True)
        self.assertTrue(self.app.activeSelection.atoms, mol.allAtoms[10:15])

        #test "xor" - from specified atomset: selects atoms that currently are not selected and deselects previously selected atoms.
        self.app.select( mol.allAtoms[:20], xor=True)
        selnames = mol.allAtoms[:10].name + mol.allAtoms[15:20].name
        
        self.assertEqual(selnames, self.app.activeSelection.atoms.name)
        # test "intersect"
        self.app.select( mol.allAtoms[15:25], intersect=True)
        # [0 1 2 3 4 5 6 7 8 9] 10 11 12 13 14 [15 16 17 18 19] 20 21 22 23 24  25 26
        #  0 1 2 3 4 5 6 7 8 9  10 11 12 13 14 [15 16 17 18 19  20 21 22 23 24] 25 26
        self.assertEqual(selnames[-5:], self.app.activeSelection.atoms.name)
        # clear selection
        self.app.GUI.clearEventFlag()
        #import pdb; pdb.set_trace()
        self.app.clearSelection()
        self.assertTrue(self.app.GUI.selectionEventCalled == True)
        
        self.assertEqual(len(self.app.activeSelection.get()),  0)

        ## FIS THIS : the following tests do not work since activeSelection is an atomSet
        # test more nodes: chain
        
        self.app.select("ind:")
        from Molkit2.protein import ChainSet, ResidueSet
        # self.assertTrue(isinstance(self.app.selection, ChainSet)
        #self.assertTrue(self.app.activeSelection.get().name == ['I'])
        # residues
        self.app.clearSelection()
        self.app.select("ind::")
        #self.assertTrue(isinstance(self.app.selection, ResidueSet))
        #self.assertTrue(self.app.selection.name == ['IND201'])
        # atoms
        self.app.clearSelection()
        self.app.select(":::C19,H30")
        from Molkit2.molecule import AtomSet
        #self.assertTrue(isinstance(self.app.selection, AtomSet))
        #self.assertTrue(self.app.selection.name == ['C19', 'H30'])

        # direct select
        self.app.clearSelection()
        mol = self.app.getMolFromName('7ins')
        if not mol:
            mol = self.app.readMolecule("Data/7ins.pdb")
        self.app.directSelect("7ins:A")
        #self.assertTrue(isinstance(self.app.selection, ChainSet))
        #self.assertTrue(self.app.selection.name == ['A'])


    def test_003_select_ivalidInput(self):
        self.app.trapExceptions=False
        mol = self.app.Mols[0]
        self.app.clearSelection()
        with self.assertRaises(AssertionError):
            self.app.select('aaa')
        with self.assertRaises(AssertionError):
            self.app.select(mol, klass='atom')
        with self.assertRaises(AssertionError):
            self.app.select(mol, xor="AAA")
        with self.assertRaises(AssertionError):
            self.app.select(mol, negate=5)
        with self.assertRaises(AssertionError):
            self.app.select(mol, intersect="ind")


class TestSelectFromString(TestBase):

    def setUp(self):
        if not hasattr(self.app, 'undo'):
            from AppFramework.notOptionalCommands import UndoCommand,\
                 RedoCommand
            self.app.addCommand(UndoCommand(), 'undo')
            self.app.addCommand(RedoCommand(), 'redo')
        if not hasattr(self.app, "GUI"):
            self.app.GUI = TestGuiApp(self.app)


    def test_001_loadCommand(self):
        """test that we can load file commands to Application"""
        #from PmvApp.Pmv import MolApp
        #app = MolApp()
        app = self.app
        app.lazyLoad('selectionCmds', commands=['select',
                     'selectFromString', 'clearSelection'],
                     package='PmvApp')
        self.assertTrue( hasattr(app, "selectFromString"))
        app.select.loadCommand()
        self.assertTrue("selectFromString" in app.commands)

    
    def test_002_select_fromString(self):
        #self.app.selectFromString(mols='ind',chains='',res='',atoms='1-10')
        app = self.app
        mol = app.getMolFromName('1crn')
        if not mol:
            mol = app.readMolecule("Data/1crn.pdb")
        app.GUI.clearEventFlag()
        app.selectFromString(mols='',chains='',res='',atoms='backbone')
        self.assertTrue(self.app.GUI.selectionEventCalled == True)
        
        # 46 residues of backbone atoms=>4*46 or 184
        # test "XOR"
        app.selectFromString(mols='',chains='',res='',atoms='N', xor=True)
        #46 residues of backbone atoms - N=>3*46 =  138
        self.assertEqual(len(app.activeSelection.atoms), 138)
        app.GUI.clearEventFlag()
        app.undo() # back to "backbone" selection - 184 atoms
        self.assertTrue(self.app.GUI.selectionEventCalled == True)
        # test "intersect" 
        app.selectFromString(mols='',chains='',res='ALA*',atoms='*',
                                 intersect=True)
        self.assertEqual(len(app.activeSelection.atoms), 20)

        app.clearSelection()
        app.selectFromString(mols='',chains='',res='ALA*',atoms='C?') # 5 atoms
        app.selectFromString(mols='',chains='',res='',atoms='backbone',
                                 xor=True)
        # 5 ALA residuesCatoms(15atoms)xor backbone atoms(184) =>184-5=>179
        self.assertEqual(len(app.activeSelection.atoms), 179)

        # test "negate"
        app.clearSelection()
        app.selectFromString(mols='',chains='',res='ALA*',atoms='*')
        app.selectFromString(mols='',chains='',res='',atoms='backbone',
                                 negate=True)
        # 5 ALA residues(25atoms)- backbone atoms(20) =>5
        self.assertEqual(len(app.activeSelection.atoms), 5)
        return
        ##### FIX THIS : teh following tests fail
        # molecule name
        app.clearSelection()
        app.readMolecule("Data/1crn_hs.pdb")
        app.selectFromString('1crn_hs',chains='',res='',atoms='')
        self.assertEqual(len(app.activeSelection.get()),1)
        self.assertEqual(app.activeSelection.atoms[0].name , '1crn_hs')

        #select proteic Chains
        app.selectFromString(mols='',chains='proteic',res='',atoms='')
        self.assertEqual(len(app.activeSelection.atoms), 2)
        from Molkit2.protein import Chain, Residue, ResidueSet
        #self.assertTrue(isinstance(app.activeSelection.get(), Chain))
        #self.assertTrue(isinstance(app.activeSelection.get(), Chain))

        app.clearSelection()
        #select dna Chains
        app.readMolecule("Data/dnaexple.pdb")
        app.selectFromString(mols='',chains='dna',res='',atoms='')

        #self.assertEqual(len(app.activeSelection.get()),1)
        #self.assertTrue(isinstance(app.activeSelection.get(), Chain))
        self.assertEqual(app.activeSelection.get().top.name, 'dnaexple')

        #select all Chains
        app.selectFromString(mols='',chains='*',res='',atoms='')
        #self.assertEqual(len(app.activeSelection.get()), 3)

        #select molecule by number
        app.clearSelection()
        app.selectFromString(mols='0',chains='',res='',atoms='')
        #self.assertEqual(len(app.activeSelection.get()),1)
        #self.assertEqual(app.activeSelection.get().name , "1crn")

        #select Chain by number
        app.clearSelection()
        app.selectFromString(mols='',chains='1',res='',atoms='')
        #self.assertEqual(len(app.activeSelection.get()),1)
        #self.assertEqual(app.activeSelection.get().top.name, '1crn_hs')

        #select Residue by number
        app.clearSelection()
        app.selectFromString(mols='',chains='',res='40',atoms='')
        #self.assertEqual(len(app.activeSelection.get()),1)
        #self.assertTrue(isinstance(app.activeSelection.get(), Residue))
        #self.assertEqual(app.activeSelection.get().name, 'PRO41')
        
        #select Atom by number
        app.clearSelection()
        app.selectFromString(mols='',chains='',res='',atoms='200')
        #self.assertEqual(len(app.activeSelection.get()),1)
        #self.assertEqual(app.activeSelection.get(), app.allAtoms[200])

        #select Res by Range
        app.clearSelection()
        app.selectFromString(mols='',chains='',res='1-10',atoms='')
        #self.assertEqual(len(app.activeSelection.get()),10)
        #self.assertTrue(isinstance(app.activeSelection.get(), Residue))

        #select Atom by Range
        from Molkit2.molecule import Atom
        app.clearSelection()
        app.selectFromString(mols='',chains='',res='',atoms='1-10')
        #self.assertEqual(len(app.activeSelection.get()),10)
        #self.assertTrue(isinstance(app.activeSelection.get(), Atom))

        #select Res by Relative Range
        app.clearSelection()
        app.selectFromString(mols='',chains='',res='#1-#10',atoms='')
        #self.assertEqual(len(app.activeSelection.get()), 30)

        #select Atoms by Relative Range
        app.clearSelection()
        app.selectFromString(mols='',chains='',res='',atoms='#1-#10')
        #from each residue this selects first 10 atoms or 0 if len(res.atoms) < 10
        #self.assertEqual(len(app.activeSelection.get()), 570)

        #select Res by Sequence
        app.clearSelection()
        app.selectFromString(mols='',chains='',res='PEA',atoms='')
        #self.assertEqual(len(app.activeSelection.get()), 6)
        #self.assertTrue(isinstance(app.activeSelection.get(), Residue))
        #self.assertTrue(app.activeSelection.get().name, 'PRO22')

        #select Res by Sequence 3
        app.selectFromString(mols='',chains='',res='TTCC,PEA,GAT',atoms='')
        #self.assertEqual(len(app.activeSelection.get()), 20)
        #self.assertTrue(app.activeSelection.get().name, 'THR1')
        #select sidechain
        app.clearSelection()
        app.selectFromString(mols='1crn',chains='',res='ALA*', atoms='sidechain')
        #self.assertTrue(app.activeSelection.get().top.uniq().name, ['1crn'])
        #self.assertTrue(app.activeSelection.get().name, ['CB', 'CB', 'CB', 'CB', 'CB'])
        # add to the selection
        app.selectFromString(mols='1crn_hs',chains='',res='ASP*',atoms='sidechain')
        #self.assertTrue(app.activeSelection.get().top.uniq().name, ['1crn', '1crn_hs'])
        #self.assertTrue(app.activeSelection.get().name, ['CB', 'CB', 'CB', 'CB', 'CB', 'CB', 'HB1', 'HB2', 'CG', 'OD1', 'OD2'])
        

    def test_003_invalidInput(self):
        
        #Chain by Name
        app = self.app
        app.clearSelection()
        app.selectFromString(mols='',chains='QQ',res='',atoms='')
        #self.assertEqual(len(app.activeSelection.get()),0)

        #select mol by number
        app.selectFromString(mols='20',chains='',res='',atoms='')
        #self.assertEqual(len(app.activeSelection.get()),0)

        #select Res by number
        app.selectFromString(mols='',chains='',res='400',atoms='')
        #self.assertEqual(len(app.activeSelection.get()),0)

        #select Atom by number
        app.selectFromString(mols='',chains='',res='',atoms='4000')
        #self.assertEqual(len(app.activeSelection.get()),0)
        #select Res by Range
        app.selectFromString(mols='',chains='',res='500-530',atoms='')
        #self.assertEqual(len(app.activeSelection.get()),0)
        
        #select Atom by Range
        app.selectFromString(mols='',chains='',res='',atoms='475463524-4344526')
        #self.assertEqual(len(app.activeSelection.get()),0)

        #select Res by Relative Range
        app.selectFromString(mols='',chains='',res='#50-#53',atoms='')
        #self.assertEqual(len(app.activeSelection.get()),0)

        #select Res by Mol Sequence
        app.selectFromString(mols='PEA',chains='',res='PIA',atoms='')
        #self.assertEqual(len(app.activeSelection.get()),0)



class TestSaveSet(TestBase):

    def test_001_loadCommand(self):
        """test that we can load file commands to Application"""
        #from PmvApp.Pmv import MolApp
        #app = MolApp()
        app = self.app
        app.lazyLoad('selectionCmds', commands=['select', 'saveSet',
                     'clearSelection', 'selectSet'],
                     package='PmvApp')
        self.assertTrue( hasattr(app, 'saveSet'))
        app.saveSet.loadCommand()
        self.assertTrue('saveSet' in app.commands)
        
        
    def test_002_saveSet(self):
        mol = self.app.getMolFromName('ind')
        if not mol:
            mol = self.app.readMolecule("Data/ind.pdb")
        self.app.clearSelection()
        self.app.saveSet(mol.allAtoms[1:20], "set1")
        self.assertTrue(self.app.sets["set1"] == mol.allAtoms[1:20])
        
        self.app.select("ind:I:IND201:C21,C22,C23,C18,C19,C20")
        self.app.saveSet("ind:I:IND201:C21,C22,C23,C18,C19,C20", "set2")
        self.assertTrue(self.app.sets["set2"] == self.app.activeSelection.get())

        self.app.clearSelection()
        self.app.selectSet("set1")
        self.assertTrue(self.app.activeSelection.get() == mol.allAtoms[1:20])


    def test_003_ivalidInput(self):
        #input nodes
        self.app.trapExceptions=False
        with self.assertRaises(AssertionError):
            self.app.saveSet("aaa", "set1")
        # set name
        with self.assertRaises(AssertionError):
            self.app.saveSet("ind:I:IND201:C21,C22,C23", self.app.Mols[0])



class TestSelectInSphere(TestBase):
    
   def test_001_loadCommand(self):
        """test that we can load file commands to Application"""
        #from PmvApp.Pmv import MolApp
        #app = MolApp()
        app = self.app
        app.lazyLoad('selectionCmds',
                     commands=['select', 'selectInSphere',
                               'clearSelection'],
                     package='PmvApp')
        self.assertTrue( hasattr(app, "selectInSphere"))
        app.select.loadCommand()
        self.assertTrue("selectInSphere" in app.commands)
    

   def test_002_selectInSphere(self):
        mol = self.app.getMolFromName('ind')
        if not mol:
            mol = self.app.readMolecule("Data/ind.pdb")
        self.app.clearSelection()
        atom = self.app.select("ind:I::O1")[0]
        # select atoms in a sphere (center - coords of the selected atom, radius == 2.)
        self.app.selectInSphere([atom.coords], 2., ['ind'])
        self.assertTrue(len(self.app.activeSelection.get()) == 2)
        # increase the radius
        self.app.selectInSphere([atom.coords], 2.4, ['ind'])
        self.assertTrue(self.app.activeSelection.get().name == ['C2', 'C3', 'O1', 'N2'])

        mol1 =  self.app.getMolFromName('1crn')
        if not mol1:
            mol1 = self.app.readMolecule("Data/1crn.pdb")
        # increase the radius, add another molecule to the list of molnames:
        self.app.selectInSphere([atom.coords], 7, ['ind', '1crn'])
        self.assertTrue(self.app.activeSelection.get().top.uniq().name == ['ind', '1crn'])
        natoms = len(self.app.activeSelection.get())
        # remove a molecule from the molname list:
        self.app.selectInSphere([atom.coords], 7, ['1crn',])
        self.assertTrue(self.app.activeSelection.get().top.uniq().name == ['1crn'])
        print("SelectInSphere",  len(self.app.Mols))
        # use default list of molecules --['all']
        self.app.readMolecule("Data/1HS1.pdb")
        self.app.selectInSphere([atom.coords], 30)
        #print len(self.app.activeSelection.get()), self.app.activeSelection.get().top.uniq().name, "n mols:", len(self.app.Mols)
        selmols = self.app.activeSelection.get().top.uniq().name
        self.assertTrue('1crn' in selmols)
        self.assertTrue('ind' in selmols)
        self.assertTrue('1HS1' in selmols)
        self.app.clearSelection()
        # select around two atoms
        self.app.select("ind:I::O1")
        self.app.select("1HS1:A:  U9:C1*")
        self.app.selectInSphere(self.app.activeSelection.get().coords, 2)
        self.assertTrue(len(self.app.activeSelection.get()) == 7)
        self.assertTrue(len(self.app.activeSelection.get().top.uniq().name) == 2)
        # the command can take centerList values in either form:
        # [x,y,z] or [[x,y,z]],  [[x1,y1,z1],...,[xn, yn, zn]]
        self.app.clearSelection()
        self.app.selectInSphere([[-2.07, 1.525, -4.464]], 1)
        self.assertTrue(self.app.activeSelection.get()[0] == atom)
        self.app.clearSelection()
        self.app.selectInSphere([-2.07, 1.525, -4.464], 1)
        self.assertTrue(self.app.activeSelection.get()[0] == atom)
        

   def test_003_ivalidInput(self):
        atom = self.app.allAtoms[0]
        self.app.trapExceptions=False
        # centerList is list, tuple or numpy.ndarray
        with self.assertRaises(AssertionError):
            self.app.selectInSphere(atom, 2)
        with self.assertRaises(AssertionError):
            self.app.selectInSphere([], 2)
        with self.assertRaises(AssertionError):
            self.app.selectInSphere([1,1,1], [2,2,2])
        with self.assertRaises(AssertionError):
            self.app.selectInSphere([1,1,1], 2 , "1crn")


class TestInvertSelection(TestBase):
    def test_001_loadCommand(self):
        """test that we can load file commands to Application"""
        #from PmvApp.Pmv import MolApp
        #app = MolApp()
        app = self.app
        app.lazyLoad('selectionCmds', commands=['select',
                    'invertSelection', 'clearSelection', 'deselect',
                     'directSelect'],
                     package='PmvApp')
        self.assertTrue( hasattr(app, "invertSelection"))
        app.select.loadCommand()
        self.assertTrue("invertSelection" in app.commands)
    
    def test_002_ivertSelection(self):
        self.app.clearSelection()
        mol1 =  self.app.getMolFromName('1crn')
        if not mol1:
            mol1 = self.app.readMolecule("Data/1crn.pdb")
        self.app.select(mol1.allAtoms[:20])
        #self.assertTrue(len(self.app.activeSelection.get()) == 20)
        allatoms = len(mol1.allAtoms)
        self.app.invertSelection('molecule')
        natoms = allatoms-20
        #self.assertTrue(len(self.app.activeSelection.get()) == natoms)

        mol2 = self.app.getMolFromName('ind')
        if not mol2:
            mol2 = self.app.readMolecule("Data/ind.pdb")
        self.app.invertSelection('all')
        #self.assertTrue(len(self.app.activeSelection.get()) == len(self.app.allAtoms)-natoms)
        self.app.clearSelection()
        mol3 = self.app.getMolFromName('7ins')
        if not mol3:
            mol3 = self.app.readMolecule("Data/7ins.pdb")
        self.app.directSelect("7ins:A")
        self.app.select(mol2.allAtoms[:10])
        natoms = len(mol3.chains[0].residues.atoms)+10
        
        self.app.invertSelection('molecule')
        #self.assertTrue(len(self.app.activeSelection.get()) == len(mol2.allAtoms)+len(mol3.allAtoms)-natoms)
        #self.assertFalse('1crn' in  self.app.activeSelection.get().top.uniq().name)
        
            
        
if __name__ == '__main__':
    import os
    os.chdir(os.path.split(testBase.__file__)[0])

    unittest.main()

        
        
        
