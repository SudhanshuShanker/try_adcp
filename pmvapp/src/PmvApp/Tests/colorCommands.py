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
# $Header: /mnt/raid/services/cvs/PmvApp/Tests/colorCommands.py,v 1.3.4.1 2017/07/13 20:50:45 annao Exp $
#
# $Id: colorCommands.py,v 1.3.4.1 2017/07/13 20:50:45 annao Exp $
#
import unittest
from . import testBase
from .testBase import TestBase
from mglutil.errors import MGLException
from AppFramework.AppCommands import CmdLoader

class ColorTests(TestBase):

    def setUp(self):
        if not hasattr(self.app, 'undo'):
            from AppFramework.notOptionalCommands import UndoCommand,\
                 RedoCommand
            self.app.addCommand(UndoCommand(), 'undo')
            self.app.addCommand(RedoCommand(), 'redo')
        if not hasattr(self.app, "displayLines"):
            self.app.lazyLoad("displayCmds", package="PmvApp") 

    def test_001_loadCommands(self):
        """test that we can load delete commands to the application"""
        #from PmvApp.Pmv import MolApp
        #app = MolApp()
        app = self.app
        cmds = ['color', 'colorByAtomType', 'colorByResidueType',
                'colorAtomsUsingDG', 'colorResiduesUsingShapely',
                'colorByChains', 'colorByMolecules', 'colorByInstance',
                'colorByProperty', 'colorRainbow', 'colorRainbowByChain',
                'colorByExpression', 'colorByLinesColor']
        app.lazyLoad("colorCmds", commands=cmds, package="PmvApp")
        for colorcmd in cmds:
            self.assertTrue(hasattr(app, colorcmd))
        cmd = getattr(app, colorcmd)
        self.assertTrue(isinstance(cmd, CmdLoader))
        cmd.loadCommand()
        self.assertTrue(colorcmd in app.commands)


    def test_002_color_geoms(self):
        """ test color diff geoms with default args"""
        mol = self.app.readMolecule("Data/1crn.pdb")
        # lines should be displayed
        atms = self.app.allAtoms
        
        self.app.displayLines(mol)
        self.assertTrue('lines' in atms.colors)

        self.app.displaySticksAndBalls(mol)
        # colors of balls & sticks should be the same as lines (how to check it? there is no
        # atms.colors['balls'] or atms.colors['sticks'] yet

        # color S & B
        self.app.color(mol, geomsToColor=['balls'], colors = [[0., 0., 1.]] )
        self.app.color(mol, geomsToColor=['sticks'], colors = [[0., 1., 0.]] )
        bcolor = [(0., 0., 1.)] *len(atms)
        scolor = [(0., 1., 0.)] *len(atms)
        self.assertSequenceEqual(atms.colors['sticks'], scolor)
        self.assertSequenceEqual(atms.colors['balls'], bcolor)
        self.app.undo()
        self.app.undo()
        self.assertSequenceEqual(atms.colors['lines'], atms.colors['balls'])
        self.assertSequenceEqual(atms.colors['lines'], atms.colors['sticks'])
        
        self.app.displayCPK(mol)
        # colors of cpk should be the same as lines
        #self.assertSequenceEqual(atms.colors['lines'], atms.colors['cpk'])
        #color cpk blue:
        self.app.color(mol, geomsToColor=['cpk'], colors = [(0., 0., 1.)] )
        colors = [(0., 0., 1.)] * len(atms)
        self.assertSequenceEqual(atms.colors['cpk'], colors)
        self.app.undo()
        self.assertSequenceEqual(atms.colors['lines'], atms.colors['cpk'])
        if not hasattr (self.app, "computeMSMS"):
            self.app.lazyLoad("msmsCmds", commands=["computeMSMS"], package="PmvApp")
        self.app.computeMSMS(mol)
        # colors of msms should be the same as lines
        #self.assertSequenceEqual(atms.colors['lines'], atms.colors['MSMS-MOL'])
        self.app.color(mol, geomsToColor=['MSMS-MOL'], colors = [[1., 1., 0.]] )
        mcolor = [(1., 1., 0.)] * len(atms)
        self.assertSequenceEqual(atms.colors['MSMS-MOL'], mcolor)
        self.app.undo()
        self.assertSequenceEqual(atms.colors['lines'], atms.colors['MSMS-MOL'])

        # color all:

        self.app.color(mol, geomsToColor=['all'], colors = [[0., 0., 1.]] )
        self.assertSequenceEqual(atms.colors['cpk'], colors)
        self.assertSequenceEqual(atms.colors['lines'], colors)
        self.assertSequenceEqual(atms.colors['balls'], colors)
        self.assertSequenceEqual(atms.colors['sticks'], colors)
        self.assertSequenceEqual(atms.colors['MSMS-MOL'], colors)


    def test_003_color_invalid_input(self):

        if not len(self.app.Mols):
            mol = self.app.readMolecule("Data/1crn.pdb")[0]
        else:
            mol = self.app.Mols[0]
        self.app.trapExceptions = False
        with self.assertRaises(AssertionError):
            # wrong nodes
            self.app.color('abc')
        with self.assertRaises(AssertionError):
            # geoms shuold be a list:
            self.app.color(mol, geomsToColor="all")
        with self.assertRaises(AssertionError):
            #colors should be a list , tuple or numpy array
            self.app.color(mol, geomsToColor=["all"], colors="blue")


    def test_004_color_byAtomType(self):
        if not len(self.app.Mols):
            mol = self.app.readMolecule("Data/1crn.pdb")[0]
        else:
            mol = self.app.Mols[0]
        from Pmv.pmvPalettes import AtomElements
        from Pmv.colorPalette import ColorPaletteNG
        palette = ColorPaletteNG('Atom Elements', colorDict=AtomElements,readonly=0, info="", lookupMember='element')
        atms = mol.allAtoms
        colors = palette.lookup(atms)
        self.app.colorByAtomType(mol, geomsToColor=['lines'])
        [self.assertSequenceEqual(tuple(color), colors[i]) for i, color in enumerate(atms.colors['lines'])]
        self.app.color(mol, geomsToColor = ['lines'], colors=[(1.,1.,1.)])
        if 'cpk' not in atms.colors:
            # if we run this test separately - there is no cpk yet 
            self.app.displayCPK(mol)
        self.app.colorByAtomType(mol, geomsToColor=['cpk'])
        [self.assertSequenceEqual(tuple(color), colors[i]) for i, color in enumerate(atms.colors['cpk'])]
        if 'balls' not in atms.colors:
            self.app.displaySticksAndBalls(mol)
        self.app.colorByAtomType(mol, geomsToColor=['balls', 'sticks'])
        [self.assertSequenceEqual(tuple(color), colors[i]) for i, color in enumerate(atms.colors['balls'])]
        [self.assertSequenceEqual(tuple(color), colors[i]) for i, color in enumerate(atms.colors['sticks'])]
        if 'MSMS-MOL' not in atms.colors:
            self.app.computeMSMS(mol)
            oldcolors = atms.colors['lines'][:]
        else:
            oldcolors = atms.colors['MSMS-MOL'][:]
        self.app.colorByAtomType(mol, geomsToColor=['MSMS-MOL'])
        [self.assertSequenceEqual(tuple(color), colors[i]) for i, color in enumerate(atms.colors['MSMS-MOL'])]
        #undo the last command
        
        self.app.undo()
        [self.assertSequenceEqual(tuple(color), oldcolors[i]) for i, color in enumerate(atms.colors['MSMS-MOL'])]

        
    def test_005_color_byDG(self):
                
        if not len(self.app.Mols):
            mol = self.app.readMolecule("Data/1crn.pdb")[0]
        else:
            mol = self.app.Mols[0]
        from Pmv.pmvPalettes import  DavidGoodsell, DavidGoodsellSortedKeys
        from Pmv.colorPalette import ColorPaletteFunctionNG
        cmd = self.app.colorAtomsUsingDG.loadCommand()
        palette = ColorPaletteFunctionNG('DavidGoodsell', DavidGoodsell, readonly=0, info="",
            sortedkeys=DavidGoodsellSortedKeys, lookupFunction=cmd.lookupFunc)
        atms = mol.allAtoms
        colors = palette.lookup(atms)
        # color lines
        cmd(mol, geomsToColor=['lines'])
        [self.assertSequenceEqual(tuple(color), colors[i]) for i, color in enumerate(atms.colors['lines'])]
        # color lines white, so if a new geometry is added , it will be the same color as lines - white
        self.app.color(mol, geomsToColor = ['lines'], colors=[(1.,1.,1.)])
        if 'cpk' not in atms.colors:
            self.app.displayCPK(mol)
        # color cpk
        cmd(mol, geomsToColor=['cpk'])
        [self.assertSequenceEqual(tuple(color), colors[i]) for i, color in enumerate(atms.colors['cpk'])]
        if 'balls' not in atms.colors:
            self.app.displaySticksAndBalls(mol)
        # color S&B
        cmd (mol, geomsToColor=['balls', 'sticks'])
        [self.assertSequenceEqual(tuple(color), colors[i]) for i, color in enumerate(atms.colors['balls'])]
        [self.assertSequenceEqual(tuple(color), colors[i]) for i, color in enumerate(atms.colors['sticks'])]
        
        if 'MSMS-MOL' not in atms.colors:
            self.app.computeMSMS(mol)
            oldcolors = atms.colors['lines'][:]
        else:
            oldcolors = atms.colors['MSMS-MOL'][:]
        # color msms
        cmd(mol, geomsToColor=['MSMS-MOL'])
        [self.assertSequenceEqual(tuple(color), colors[i]) for i, color in enumerate(atms.colors['MSMS-MOL'])]
        #undo the last command ]
        self.app.undo()
        [self.assertSequenceEqual(tuple(color), oldcolors[i]) for i, color in enumerate(atms.colors['MSMS-MOL'])]



    def test_006_color_byResidue(self):
        if not len(self.app.Mols):
            mol = self.app.readMolecule("Data/1crn.pdb")[0]
        else:
            mol = self.app.Mols[0]
        from Molkit2.protein import ResidueSet
        from Pmv.pmvPalettes import RasmolAmino
        resDict = {}
        resList = ['CYS', 'ILE', 'SER', 'VAL', 'PRO', 'THR', 'PHE', 'GLU', 'GLY', 'ASP', 'LEU', 'ARG', 'ALA', 'ASN', 'TYR']
        for res in resList:
           resDict[res] =  ResidueSet([x for x in mol.chains.residues if x.type == res])
        atms = mol.allAtoms
        if 'cpk' not in atms.colors:
            self.app.displayCPK(mol)

        if 'balls' not in atms.colors:
            self.app.displaySticksAndBalls(mol)

        if 'MSMS-MOL' not in atms.colors:
            self.app.computeMSMS(mol)
        # color all geometries
        self.app.colorByResidueType(atms, ['all'])
        for geom in ['lines', 'cpk', 'balls', 'sticks', 'MSMS-MOL']:
            for res in resList:
                color  = RasmolAmino[res]
                # check that atoms of each residue has color from RasmoAmino dictioanary
                for rescolor in resDict[res].atoms.colors[geom]:
                    self.assertSequenceEqual(color, tuple(rescolor))
                    #print geom, res, color, tuple(rescolor)

        
    def test_007_color_ByShapely(self):
        if not len(self.app.Mols):
            mol = self.app.readMolecule("Data/1crn.pdb")[0]
        else:
            mol = self.app.Mols[0]
        from Molkit2.protein import ResidueSet
        from Pmv.pmvPalettes import Shapely
        resDict = {}
        resList = ['CYS', 'ILE', 'SER', 'VAL', 'PRO', 'THR', 'PHE', 'GLU', 'GLY', 'ASP', 'LEU', 'ARG', 'ALA', 'ASN', 'TYR']
        for res in resList:
           resDict[res] =  ResidueSet([x for x in mol.chains.residues if x.type == res])
        atms = mol.allAtoms
        if 'cpk' not in atms.colors:
            self.app.displayCPK(mol)

        if 'balls' not in atms.colors:
            self.app.displaySticksAndBalls(mol)

        if 'MSMS-MOL' not in atms.colors:
            self.app.computeMSMS(mol)
        # color all geometries
        self.app.colorResiduesUsingShapely(atms, ['all'])
        for geom in ['lines', 'cpk', 'balls', 'sticks', 'MSMS-MOL']:
            for res in resList:
                color  = Shapely[res]
                # check that atoms of each residue has color from Shapely dictioanary
                for rescolor in resDict[res].atoms.colors[geom]:
                    self.assertSequenceEqual(color, tuple(rescolor))
                    #print geom, res, color, tuple(rescolor)


    def test_008_color_ByChain(self):
        mol = self.app.readMolecule("Data/7ins.pdb")[0]
        from mglutil.util.defaultPalettes import MolColors
        atms = mol.allAtoms
        self.app.displayLines(mol)
        self.app.displayCPK(mol)
        self.app.displaySticksAndBalls(mol)
        self.app.computeMSMS(mol)
        # color all geometries
        self.app.colorByChains(atms, ['all'])
        for chain in mol.chains:
            number = str(chain.number)
            chcolor =  MolColors[number]
            for geom in ['lines', 'cpk', 'balls', 'sticks', 'MSMS-MOL']:
                atcolors = chain.residues.atoms.colors[geom]
                for color in atcolors:
                    self.assertSequenceEqual(color, chcolor)


    def test_009_color_ByMolecule(self):
        mol1 =  self.app.getMolFromName('1crn')
        if not mol1:
            mol1 = self.app.readMolecule("Data/1crn.pdb")[0]
            self.app.displayCPK(mol1)
            self.app.displaySticksAndBalls(mol1)
            self.app.computeMSMS(mol1)
        mol2 =  self.app.getMolFromName('7ins')
        if not mol2:
            mol2 = self.app.readMolecule("Data/7ins.pdb")[0]
            self.app.displayCPK(mol2)
            self.app.displaySticksAndBalls(mol2)
            self.app.computeMSMS(mol2)

        from mglutil.util.defaultPalettes import MolColors
        
        # color all geometries
        self.app.colorByMolecules("1crn:::/+/7ins:::",  ['all'])
        for i, mol  in enumerate([mol1, mol2]):
            molcolor =  MolColors[str(i)]
            for geom in ['lines', 'cpk', 'balls', 'sticks', 'MSMS-MOL']:
                atcolors = mol.allAtoms.colors[geom]
                cd = {}.fromkeys(['%f%f%f'%tuple(c) for c in atcolors])
                self.assertEqual (len(cd), 1)
                self.assertSequenceEqual(atcolors[0], molcolor)

            

    def test_010_color_byProperty(self):
                
        if not len(self.app.Mols):
            mol = self.app.readMolecule("Data/1crn.pdb")[0]
            self.app.computeMSMS(mol)
            oldcolors = mol.allAtoms.colors['lines'][:]
        else:
            mol = self.app.Mols[0]
            oldcolors = mol.allAtoms.colors['MSMS-MOL'][:]
        atms = mol.allAtoms
        mini = 3.38
        maxi=23.9
        self.app.colorByProperty(mol, ['MSMS-MOL'], 'temperatureFactor',
                                colormap='rgb256', mini=mini, maxi=maxi)
        propvalues = mol.allAtoms.temperatureFactor
        colormap = self.app.colorMaps['rgb256']
        colors = colormap.Map(propvalues, mini=mini, maxi=maxi)
        #print self.app.colorMaps['rgb256'].mini, self.app.colorMaps['rgb256'].maxi
        #print colors[:5]
        [self.assertSequenceEqual(color, tuple(colors[i][:3]) ) for i, color in enumerate(atms.colors['MSMS-MOL'])]

        #undo the command , msms should be colored the same color as before
        self.app.undo()
        [self.assertSequenceEqual(color , oldcolors[i]) for i, color in enumerate(atms.colors['MSMS-MOL'])]
        self.app.trapExceptions = False
        # test wrong arguments:
        with self.assertRaises(AssertionError):
            self.app.colorByProperty(mol, ['MSMS-MOL'], 5)
        with self.assertRaises(AssertionError):
            self.app.colorByProperty(mol, ['MSMS-MOL'], 'temperatureFactor', propertyLevel='atom' )
        with self.assertRaises(AssertionError):
            self.app.colorByProperty(mol, ['MSMS-MOL'], 'temperatureFactor', mini=5, maxi=2)
        with self.assertRaises(AssertionError):
            self.app.colorByProperty(mol, ['MSMS-MOL'], 'temperatureFactor', colormap='RGB')
        # test error  in property value:
        tf = mol.allAtoms[2].temperatureFactor
        del(mol.allAtoms[2].temperatureFactor)
        with self.assertRaises(RuntimeError):
            self.app.colorByProperty(atms, ['MSMS-MOL'], 'temperatureFactor')
        mol.allAtoms[2].temperatureFactor = tf


        


if __name__ == '__main__':
    import os
    os.chdir(os.path.split(testBase.__file__)[0])

    unittest.main()
