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

import sys, unittest, time

from MolKit2 import Read

class deleteAtomsTests(unittest.TestCase):

    """
    delete atoms
    """
    def deleteAtoms(self):
        mol = Read('Data/1crn.pdb')
        molLen = len(mol._ag)
        sel = mol.select('resnum 3 4 5')
        assert len(mol.select())==molLen
        l = len(sel)
        assert l==19
        mol.deleteAtoms(sel)
        assert len(mol.select())==(molLen-l)

        mol.undeleteAtoms(sel)
        assert len(mol.select())==molLen

class deleteCopyMolecule(unittest.TestCase):
    """
    delete atoms
    """
    def cloneMolecule(self):
        mol = Read('Data/1crn.pdb')
        newMol = mol.clone('copy')
        assert len(mol._ag) == len(newMol._ag)
        assert len(mol._ag._bonds) == len(newMol._ag._bonds)
        
    def cloneMoleculeAfterDelete(self):
        mol = Read('Data/1crn.pdb')
        molLen = len(mol._ag)
        sel = mol.select('resnum 3 4 5')
        l = len(sel)
        mol.deleteAtoms(sel)
        newMol = mol.clone('copy')
        assert len(newMol._ag)==(molLen-l)
        assert max(newMol._ag._bonds.flatten()) == len(newMol._ag)-1
        
        
class AddAtoms(unittest.TestCase):

    """
    delete atoms
    """
    def deleteAtoms(self):
        mol = Read('Data/1crn.pdb')

        mol1 = mol.select('resnum 1 2 3').toMolecule()
        sel = mol.select('resnum 3 4 5')

        mol1.addAtoms(sel)

if __name__ == '__main__':
    unittest.main()
