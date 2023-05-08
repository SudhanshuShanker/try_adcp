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

import unittest, sys
from .testBase import TestBase
from mglutil.errors import MGLException


class TestBondsCmds(TestBase):

    def test_001_loadCommands(self):
        """test that we can load PmvApp/bondsCmds to the application"""
        #from PmvApp.Pmv import MolApp
        #app = MolApp()
        app = self.app
        app.lazyLoad('bondsCmds', package='PmvApp')
        from AppFramework.AppCommands import CmdLoader
        for key in ['addBondsGC', 'buildBondsByDistance', 'removeBondsGC', 'removeBonds', 'addBonds']:
            self.assertTrue(hasattr(app, key))
            cmd = getattr(app, key)
            self.assertTrue(isinstance(cmd, CmdLoader))
            cmd.loadCommand()
            self.assertTrue(key in app.commands)
            

    def test_002_buildBondsByDistance(self):
        """ tests the command """
        app = self.app
        mol = app.readMolecule("Data/1crn.pdb")
        app.buildBondsByDistance(mol, display = 0)
        self.assertTrue(len(mol.allAtoms.bonds[0]) == 337)


    def test_003_BuildBondsByDistance_invalid_input(self):
    
        """
        tests BuildBondsByDistance,invalid input nodes
        """
        # Should it railse an error?
        #Currently it just returns an empty list of bonds
        bonds = self.app.buildBondsByDistance("aaa", 0)
        self.assertEqual(bonds, [])


    def test_004_addBonds(self):
        mol = self.app.readMolecule("Data/1crn.pdb")[0]
        name = mol.name
        at1 = mol.NodesFromName("%s: :ALA38:N"%name)[0]
        at2 = mol.NodesFromName("%s: :THR28:CG2"%name)[0]
        nbonds = len(mol.allAtoms.bonds[0])
        self.assertTrue(len(at1.bonds) == 0)
        self.assertTrue(len(at2.bonds) == 0)
        self.app.addBonds([(at1, at2)])
        self.assertTrue(len(at1.bonds) == 1)
        self.assertTrue(len(at2.bonds) == 1)
        self.assertTrue(len(mol.allAtoms.bonds[0]) == nbonds+1)
        self.assertTrue(at1.isBonded(at2))
        # test undo
        
        
    def test_005_removeBonds(self):
        mol = self.app.readMolecule("./Data/small1crn.pdb")
        self.app.buildBondsByDistance(mol, 0)
        nbonds = len(mol.allAtoms.bonds[0])
        atm1 = self.app.expandNodes("small1crn: :THR1:CA")[0]
        atm2 = self.app.expandNodes("small1crn: :THR1:CB")[0]
        
        self.app.removeBonds([atm1.bonds[0]])
        self.assertEqual(atm1.isBonded(atm2),False)
        self.assertTrue(len(mol.allAtoms.bonds[0]) == nbonds-1)
        #test undo
    
    


#this should be true after display command is called
#self.assertEqual(len(mol.geomContainer.atoms['bonded']),327)
if __name__ == '__main__':
    import os, testBase
    os.chdir(os.path.split(testBase.__file__)[0])
    unittest.main()

