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
# $Header: /mnt/raid/services/cvs/PmvApp/Tests/msmsCommands.py,v 1.2.4.1 2017/07/13 20:50:45 annao Exp $
#
# $Id: msmsCommands.py,v 1.2.4.1 2017/07/13 20:50:45 annao Exp $
#
import unittest
from . import testBase
from .testBase import TestBase
from mglutil.errors import MGLException

def executionReportEventHandler(event):
    report = event.report
    if report.numberOf['errors']:
        from AppFramework.AppCommands import AppError
        for error in report.reports:
            if error.__class__ == AppError:
                raise error.exception
    
class ComputeMSMS(TestBase):
    def setUp(self):
        self.app.trapExceptions = False
        
    def test_001_loadCommands(self):
        """test that we can load MSMS commands to the application"""
        #from PmvApp.Pmv import MolApp
        #app = MolApp()
        app = self.app
        cmd = 'computeMSMS'
        app.lazyLoad('msmsCmds', commands=[cmd], package='PmvApp')
        self.assertTrue(hasattr(app, cmd))
        self.assertTrue(cmd in app.commands)
        cmd = getattr(app, cmd)
        from AppFramework.AppCommands import CmdLoader
        self.assertTrue(isinstance(cmd, CmdLoader))
        cmd.loadCommand()


    def test_002_computeMSMS(self):
        mol = self.app.readMolecule('Data/1crn.pdb')[0]
        gc = mol.geomContainer
        # nodes - molecule
        sName = 'MSMS1'
        self.app.computeMSMS('1crn', surfName=sName, perMol=1, density=3.0,
                            pRadius=1.5, display=0)
        self.assertEqual(sName in gc.msms,True)
        self.assertEqual(sName in gc.msmsAtoms,True)
        self.assertEqual(mol.geomContainer.msmsAtoms[sName],mol.allAtoms)

        #nodes - atom set
        sName = 'MSMS2'
        #import pdb; pdb.set_trace()
        # Select residue 1 through 10
        nodes = mol.chains[0].residues[:10]
        self.app.computeMSMS(nodes, sName, perMol=1, density=1.0,
                   pRadius=1.5, display=0)
        self.assertEqual(sName in gc.msmsAtoms,True)
        self.assertEqual(mol.geomContainer.msmsAtoms[sName],mol.allAtoms)
        surf = gc.msms[sName][0]
        self.assertEqual(surf.density, 1.0)
        self.assertEqual(surf.probeRadius, 1.5)
        # change some of the parameters:
        self.app.computeMSMS(nodes, sName, perMol=1, density=3.0,
                   pRadius=2.0, display=0)
        surf = gc.msms[sName][0]
        self.assertEqual(surf.density, 3.0)
        self.assertEqual(surf.probeRadius, 2.0 )

        mol1 = self.app.readMolecule("Data/7ins.pdb")[0]
        gc1 = mol1.geomContainer
        sName = "MSMS3"
        # noHetatm=True
        self.app.computeMSMS("7ins", sName, perMol=1, density=3.0,
                   pRadius=2.0, display=0, noHetatm=True)

        self.assertTrue(len(mol1.geomContainer.msmsAtoms[sName]) < len(mol1.allAtoms))
        surf1 = mol1.geomContainer.msms[sName][0]
        self.assertTrue(len(mol1.geomContainer.msmsAtoms[sName]) == len(surf1.coords))

        # noHetatm=False (default)
        self.app.computeMSMS("7ins", sName, perMol=1, density=3.0,
                   pRadius=2.0, display=0)

        self.assertTrue(len(mol1.geomContainer.msmsAtoms[sName]) == len(mol1.allAtoms))
        surf1 = mol1.geomContainer.msms[sName][0]
        self.assertTrue(len(mol1.geomContainer.msmsAtoms[sName]) == len(surf1.coords))
        # perMol ??? (this is always 1 in pmv)
        

    def test_003_invalid_input(self):
        #nodes
        #with self.assertRaises(AssertionError):
        #    self.app.computeMSMS("aaa", "MSMS")
        # surfName
        with self.assertRaises(AssertionError):
            self.app.computeMSMS("1crn", self.app.Mols[0])
        # pRadius
        with self.assertRaises(AssertionError):
            self.app.computeMSMS("1crn", pRadius=[1,5,4])
        
        with self.assertRaises(AssertionError):
            self.app.computeMSMS("1crn", pRadius=0)
        #display
        with self.assertRaises(AssertionError):
            self.app.computeMSMS("1crn", display="selection")
        # hdset - string (name of a set)
        with self.assertRaises(AssertionError):
            self.app.computeMSMS("1crn", hdset=self.app.allAtoms[:10])


class DisplayMSMS(TestBase):
    def setUp(self):
        if not hasattr (self.app, 'displayLines'):
            self.app.lazyLoad("displayCmds", commands=['displayLines'], package="PmvApp")
        self.app.trapExceptions = False
    
    def test_001_loadCommands(self):
        """test that we can load MSMS commands to the application"""
        #from PmvApp.Pmv import MolApp
        #app = MolApp()
        app = self.app
        cmds = ['computeMSMS', 'displayMSMS']
        app.lazyLoad('msmsCmds', commands=cmds, package='PmvApp')
        for cmd in cmds:
            self.assertTrue(hasattr(app, cmd))
            self.assertTrue(cmd in app.commands)
            cmd = getattr(app, cmd)
            from AppFramework.AppCommands import CmdLoader
            self.assertTrue(isinstance(cmd, CmdLoader))
            cmd.loadCommand()


    def test_002_displayMSMS(self):
        mol = self.app.readMolecule('Data/1crn.pdb')[0]
        # compute the surface first:
        self.app.computeMSMS(mol, display=0)
        # then display it - use default values
        self.app.displayLines(mol)
        #import pdb; pdb.set_trace()
        self.app.displayMSMS(mol)
        gc = mol.geomContainer
        self.assertTrue("MSMS-MOL" in gc.geoms)
        surf = gc.geoms["MSMS-MOL"]
        nverts = 6044
        nfaces = 12084
        self.assertTrue(len(surf.vertexSet) == nverts)
        self.assertTrue(len(surf.faceSet) == nfaces)
        #the surface is colored the same as lines
        # prop[1] == array([[ 1.,  1.,  1.,  1.]], dtype=float32)
        self.assertTrue(len(surf.materials[1028].prop[1]) == 1)
        self.assertTrue(sum(surf.materials[1028].prop[1][0]) == 4.0)
        

        # recompute the surface with different parameters and display it again:
        d = gc.msms["MSMS-MOL"][0].density
        pr = gc.msms["MSMS-MOL"][0].probeRadius
        self.app.computeMSMS(mol, density=d+1)
        self.app.displayMSMS(mol)
        # we should have more vertces and faces
        surf = gc.geoms["MSMS-MOL"]
        nverts1 = len(surf.vertexSet)
        nfaces1 = len(surf.faceSet)
        self.assertTrue(nverts1 > nverts)
        self.assertTrue(nfaces1  > nfaces)
        self.app.computeMSMS(mol, pRadius=pr+1)
        self.app.displayMSMS(mol)
        surf = gc.geoms["MSMS-MOL"]
        nverts2 = len(surf.vertexSet)
        nfaces2 =len(surf.faceSet)
        self.assertTrue(nverts2 < nverts1)
        self.assertTrue(nfaces2 < nfaces1)

        # test "negate": undisplay the surface
        self.app.displayMSMS(mol, negate=True)
        self.assertTrue(surf.visible == 0)

        nodes = mol.allAtoms[30:60]
        # test "only": display surface for a set of atoms
        self.app.displayMSMS(nodes, only=1)
        self.assertEqual(mol.geomContainer.msmsAtoms["MSMS-MOL"], mol.allAtoms)
        self.assertEqual(gc.atoms["MSMS-MOL"],  nodes)
        self.assertTrue(surf.visible == 1)
        nverts3 = len(surf.vertexSet)
        nfaces3 =len(surf.faceSet)
        self.assertTrue(nverts3 == nverts2)
        self.assertTrue(nfaces3 < nfaces2)
        #display the whole surface
        self.app.displayMSMS(mol, only=1)
        nverts4 = len(surf.vertexSet)
        nfaces4 = len(surf.faceSet)
        self.assertTrue(nverts4 == nverts2)
        self.assertTrue(nfaces4 == nfaces2)

        # test 'negate':  undisplay the surface for a set of atoms:
        self.app.displayMSMS(nodes, negate=1)
        nfaces5 = len(surf.faceSet)
        self.assertTrue(nfaces5 < nfaces2 and nfaces5 > nfaces3)
        self.assertEqual(gc.atoms["MSMS-MOL"],  mol.allAtoms-nodes)
        
        # display MSMS for 2 molecules:
        mol1 = self.app.readMolecule('./Data/1bsr.pdb')[0]

        from AppFramework.AppCommands import ExecutionReportEvent
        self.app.eventHandler.registerListener(ExecutionReportEvent,
                             executionReportEventHandler)
        sname = "molsurf"
        # check that dispaly command raises RuntimeError for a surface name that
        # does not exist:
        with self.assertRaises( RuntimeError ):
            self.app.displayMSMS("1crn,1bsr", surfName=sname)
        
        #self.app.computeMSMS(self.app.activeSelection.get(), surfName=sname, display=0)
        self.app.displayLines(mol1)
        #import pdb; pdb.set_trace()
        self.app.computeMSMS("1crn,1bsr", surfName=sname, display=0)
        self.app.displayMSMS("1crn,1bsr", surfName=sname)
        self.assertTrue(sname in mol.geomContainer.geoms)
        self.assertTrue(len(mol.geomContainer.geoms[sname].vertexSet) == 6044)
        self.assertTrue(len(mol.geomContainer.geoms[sname].faceSet) == 12084)
        self.assertTrue(sname in mol1.geomContainer.geoms)
        self.assertTrue(len(mol1.geomContainer.geoms[sname].vertexSet) == 29725)
        self.assertTrue(len(mol1.geomContainer.geoms[sname].faceSet) == 59454)
        # delete atoms event
        nodes = mol.chains[0].residues[:5]
        allatoms = len(mol.allAtoms)
        natoms = len(nodes.atoms)
        if not hasattr(self.app, "deleteAtoms"):
            self.app.lazyLoad("deleteCmds", commands=["deleteAtoms",], package="PmvApp")
        self.app.deleteAtoms(nodes)
        self.assertTrue(len(mol.geomContainer.msmsAtoms[sname]) == allatoms-natoms)
        self.assertTrue(len(mol.geomContainer.geoms[sname].vertexSet) != 6044)
        self.assertTrue(len(mol.geomContainer.geoms[sname].faceSet) != 12084)
        # check surfName "all", None
        self.app.displayMSMS("1crn", surfName="all", negate=True)
        self.assertTrue(mol.geomContainer.geoms['MSMS-MOL'].visible == 0)
        self.assertTrue(mol.geomContainer.geoms[sname].visible == 0)

        self.app.displayMSMS("1crn", surfName=None) # None in this case is the same as "all"
        self.assertTrue(mol.geomContainer.geoms['MSMS-MOL'].visible == 1)
        self.assertTrue(mol.geomContainer.geoms[sname].visible == 1)
        
        
    def test_003_invalid_input(self):
        #invalid nodes:
        #with self.assertRaises(AssertionError):
        #    self.app.displayMSMS("aaa")
        mol = self.app.Mols[0]
        #surfName
        with self.assertRaises(AssertionError):
            self.app.displayMSMS("1crn", surfName=mol)
        # only 
        with self.assertRaises(AssertionError):
            self.app.displayMSMS(mol, only="1crn")
        #negate
        with self.assertRaises(AssertionError):
            self.app.displayMSMS(mol, negate="1crn")
        #nbVert
        with self.assertRaises(AssertionError):
            self.app.displayMSMS(mol, nbVert=1.5)
        
