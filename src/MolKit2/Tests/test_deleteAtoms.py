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

from MolKit import Read

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
        
class ColorTests(ColorBaseTests):

#widget buttons  check    
    def xtest_color_geomsGUI_widget(self):
        """checks color widget is diplayed
        """
        self.mv.readMolecule("./Data/1crn.pdb")
        self.assertEqual(len(self.mv.Mols), 1)
        c=self.mv.color
        # Create the Select Geometry Inputform
        f= c.showForm('geomsGUI', modal=0, blocking=0, force=1)
        # this is to leanup the self.expamndednodes_____Atoms etc...
        c.cleanup()
        ebn = f.descr.entryByName
        # Need to do this otherwise the form closes before the assert
        button = ebn[0]['widget']
        button.wait_visibility(button)
        # Testing that the form is open
        self.assertEqual(f.root.winfo_ismapped(),1)
        f.withdraw()
