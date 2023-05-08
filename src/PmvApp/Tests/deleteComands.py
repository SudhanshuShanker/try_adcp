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
# $Header: /mnt/raid/services/cvs/PmvApp/Tests/deleteComands.py,v 1.2.4.1 2017/07/13 20:50:45 annao Exp $
#
# $Id: deleteComands.py,v 1.2.4.1 2017/07/13 20:50:45 annao Exp $
#
import unittest
from .testBase import TestBase
from mglutil.errors import MGLException
from AppFramework.AppCommands import CmdLoader


class DeleteTests(TestBase):

    def setUp(self):
        if not hasattr(self.app, 'undo'):
            from AppFramework.notOptionalCommands import UndoCommand,\
                 RedoCommand
            self.app.addCommand(UndoCommand(), 'undo')
            self.app.addCommand(RedoCommand(), 'redo')

    def test_001_loadCommands(self):
        """test that we can load delete commands to the application"""
        #from PmvApp.Pmv import MolApp
        #app = MolApp()
        app = self.app
        app.lazyLoad('deleteCmds', commands=['deleteMolecules'], package='PmvApp')
        self.assertTrue(hasattr(app, 'deleteMolecules'))
        cmd = getattr(app, 'deleteMolecules')
        self.assertTrue(isinstance(cmd, CmdLoader))
        cmd.loadCommand()
        self.assertTrue('deleteMolecules' in app.commands)


    def test_002_deleteMolecule(self):
        self.app.readMolecule('./Data/7ins.pdb')
        self.app.readMolecule('./Data/1crn.pdb')
        self.assertTrue(len(self.app.Mols) == 2)

        self.app.deleteMolecules("1crn")
        self.assertTrue(len(self.app.Mols) == 1)

        self.app.readMolecule('./Data/1crn.pdb')
        self.app.deleteMolecules("1crn,7ins")
        self.assertTrue(len(self.app.Mols) == 0)
        return
        # deleteMolecules with "unduable=True" is not working
        # need to reimplement app.getStateCodeForMolecule()
        mol = self.app.readMolecule('./Data/7ins.pdb')
        natoms = len(mol.allAtoms)
        if not hasattr(self.app, "displayLines"):
            self.app.lazyLoad("displayCmds", commands=["displayLines",], package="PmvApp")
        self.app.displayLines(mol)
        geom  = mol[0].geomContainer.geoms['bonded']
        nfaces = len(geom.faceSet)
        #import pdb; pdb.set_trace()
        self.app.deleteMolecules(mol, undoable=True)
        self.assertTrue(len(self.app.Mols) == 0)

        self.app.undo()
        self.assertTrue(len(self.app.Mols) == 1)
        mol = self.app.getMolFromName("7ins")
        self.assertTrue(mol != None)
        self.assertTrue(len(mol.allAtoms) == natoms)
        self.app.displayLines(mol)
        geom = mol.geomContainer.geoms['bonded']
        self.assertTrue(len(geom.vertexSet) == natoms)

        
if __name__ == '__main__':
    import os
    os.chdir(os.path.split(testBase.__file__)[0])

    unittest.main()
