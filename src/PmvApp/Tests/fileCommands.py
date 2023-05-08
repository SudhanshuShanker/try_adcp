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

class TestFileCmds(TestBase):

    def test_001_loadCommands(self):
        """test that we can load file commands to Application"""
        #from PmvApp.Pmv import MolApp
        #app = MolApp()
        app = self.app
        app.lazyLoad('fileCmds', commands=['readMolecules', 'readPmvSession', 'fetch', 'readAny', 'writePDB'], package='PmvApp')
        app.readMolecules.loadCommand()
        self.assertTrue("readMolecules" in app.commands)
        app.fetch.loadCommand()
        self.assertTrue("fetch" in app.commands)
        app.readPmvSession.loadCommand()
        self.assertTrue("readPmvSession" in app.commands)
        app.readAny.loadCommand()
        self.assertTrue("readAny" in app.commands)
        app.writePDB.loadCommand()
        self.assertTrue("writePDB" in app.commands)


    def test_002_readMolecules(self):
        app = self.app
        mols = app.readMolecules(["Data/1crn.pdb",])        
        self.assertTrue(len(mols)==1)
        self.assertTrue(len(self.app.Mols) == 1)
        self.assertTrue(self.app.Mols[0].name == "1crn")


    def test_003_readMoleculesError(self):
        # test bad arguments
        self.app.trapExceptions=False
        with self.assertRaises(AssertionError):
            self.app.readMolecules('foo')

        # not a list
        with self.assertRaises(AssertionError):
            self.app.readMolecules(12)

        # not a list of strings
        with self.assertRaises(AssertionError):
            self.app.readMolecules(['1crn.pdb', 12])

        # missing file
        self.app.readMolecules(['1crnasda.pdb'])
        self.assertTrue(type(self.app._executionReport.getErrors()[0].exception) == IOError)

        # bad saveAsModels
        with self.assertRaises(AssertionError):
            self.app.readMolecules(['Data/1crn.pdb'], modelsAs=True)

        # read molecule with problem
        mol = self.app.readMolecules(["Data/error.pdb"])
        self.assertTrue(type(self.app._executionReport.getErrors()[0].exception)) == ValueError
        
        # read molecule with problematic molecule in the middle
        # we should get an MGLException as the default errorHandling is 'raise'
        # read molecule with problematic molecule in the middle
        # we should still get 2 molecules
        mols = self.app.readMolecules(['Data/ind.pdb', "Data/error.pdb",
                                     'Data/protease.pdb'])
        self.assertTrue(type(self.app._executionReport.getErrors()[0].exception)) == ValueError
        self.assertTrue(len(mols)==2)
        # error in hydrogen bond record:
        # FIX THIS :error in try-exept of MolKit/pdbParser.py "Unable to parse Hydrogen Bond Record"
        mols = self.app.readMolecules(['Data/hbonds_error.pdb'])
        # error: no atom records:
        mols = self.app.readMolecules(['Data/noatom.pdb'])
        self.assertTrue(type(self.app._executionReport.getErrors()[0].exception)) == AssertionError


    def test_003read_moleculesPDBQT(self):
        # read a pdbqt file 
        mols = self.app.readMolecules(["Data/1dwb_rec.pdbqt",])
        self.assertEqual(len(mols),1)
        nmols = len(self.app.Mols)
        
        # delete this molecule
        #self.app.deleteMolecule(mols[0])
        #self.assertEqual(len(self.app.Mols),nmols-1)
        
        # read a multi model pdbqt file. "modulesAs" by default is molecule
        # this should return 9 molecules
        mols = self.app.readMolecules(["Data/ind_vina.pdbqt",])
        self.assertEqual(len(mols), 9)
        
        # read the same file with modulesAs == conformation
        mols = self.app.readMolecules(["Data/ind_vina.pdbqt",], modelsAs='conformations')
        self.assertEqual(len(mols),1)


    def test_004read_moleculesPQR(self):
        mols = self.app.readMolecules(['Data/mead.pqr'])
        self.assertEqual(len(mols),1)

        
        

if __name__ == '__main__':
    import os, testBase
    os.chdir(os.path.split(testBase.__file__)[0])
    unittest.main()
