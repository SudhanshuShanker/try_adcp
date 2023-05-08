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
# $Header: /mnt/raid/services/cvs/PmvApp/Tests/displayCommands.py,v 1.4.4.1 2017/07/13 20:50:45 annao Exp $
#
# $Id: displayCommands.py,v 1.4.4.1 2017/07/13 20:50:45 annao Exp $
#
import unittest
from .testBase import TestBase
from mglutil.errors import MGLException
from AppFramework.AppCommands import CmdLoader

class DisplayLines(TestBase):
    def test_001_loadCommands(self):
        """test that we can load the display commands to Application"""
        #from PmvApp.Pmv import MolApp
        #app = MolApp()
        app = self.app
        app.lazyLoad('displayCmds', commands=['displayLines', 'undisplayLines'], package='PmvApp')
        for key in ['displayLines', 'undisplayLines']:
            self.assertTrue(hasattr(app, key))
            cmd = getattr(app, key)
            self.assertTrue(isinstance(cmd, CmdLoader))
            cmd.loadCommand()
            self.assertTrue(key in app.commands)
        
                    

    def test_002_display_lines(self):
        """ test displayLines with default args"""
        #lineWidth=2, displayBO=False , only=False,
        #      negate=False, redraw=True
        #print " DisplayLines", self.app.Mols
        #self.app._onAddObjectCmds['Molecule'] = self.app.onAddObjectCmds['Molecule'][:]
        #self.app.onAddObjectCmds['Molecule'] = [] # so when a molecule is added to the Viewer
        # lines are not displayed
        mol = self.app.readMolecule("Data/1crn.pdb")
        self.app.buildBondsByDistance(mol)
        
        
        self.app.displayLines(mol)
        geom  = mol[0].geomContainer.geoms['bonded']
        nfaces = len(geom.faceSet)
        self.assertTrue(nfaces > 0) ## 337
        self.assertTrue(len(geom.vertexSet) == len(mol.allAtoms))       
        # default value for lines width (2)
        self.assertTrue(geom.lineWidth == 2)
        # test undo
        #self.app.NEWundo()
        #self.assertTrue(len(geom.faceSet) == 0)
        # test redo
        #self.app.redo()
        #self.assertTrue(len(geom.faceSet) == nfaces)
        

    def test_003_display_lines(self):
        """ test displayLines with invalid args"""
        mol = self.app.Mols[0]
        self.app.trapExceptions = False
        # lineWidth
        with self.assertRaises(AssertionError):
            self.app.displayLines(mol, lineWidth=None)
        with self.assertRaises(AssertionError):
            self.app.displayLines(mol, lineWidth=-1)
        #displayBO
        with self.assertRaises(AssertionError):
            self.app.displayLines(mol, displayBO=None)
        #only
        with self.assertRaises(AssertionError):
            self.app.displayLines(mol, only="None")
        #negate
        with self.assertRaises(AssertionError):
            self.app.displayLines(mol, negate="None")


    def test_004_display_lines(self):
        """ test displayLines: arguments"""
        #self.app.onAddObjectCmds['Molecule'] = self.app._onAddObjectCmds['Molecule']
        mol = self.app.Mols[0]
        # lineWidth
        self.app.displayLines(mol, lineWidth=5)
        geom = mol.geomContainer.geoms['bonded']
        self.assertTrue(geom.lineWidth == 5)
        #only
        mol1 = self.app.readMolecule("Data/7ins.pdb")
        #self.app.buildBondsByDistance(mol1)
        self.app.displayLines(mol1.chains[0], only=True)
        geom1 = mol1[0].geomContainer.geoms['bonded']
        allatms = len(mol1.allAtoms)
        chainatms = len(mol1.chains[0].residues.atoms)
        self.assertTrue(len(geom1.vertexSet) == chainatms)
        self.app.displayLines(mol1, only=False)
        self.assertTrue(len(geom1.vertexSet) == allatms)
        #negate
        self.app.displayLines(mol1.chains[0], only = False, negate =True)
        self.assertTrue(len(geom1.vertexSet) == allatms-chainatms)
        #displayBO
        mol2 = self.app.readMolecule("Data/hpi1s.mol2" )
        #self.app.buildBondsByDistance(mol2)       
        self.app.displayLines(mol2, displayBO=False)
        bogeom = mol2[0].geomContainer.geoms['bondorder']
        self.assertTrue(len(bogeom.vertexSet)==0)
        self.assertTrue(len(bogeom.faceSet)==0)
        self.app.displayLines(mol2, displayBO=True)
        self.assertTrue(len(bogeom.vertexSet)== 26)
        self.assertTrue(len(bogeom.faceSet)==13)


class DisplayCPK(TestBase):
    
    def test_001_loadCommands(self):
        """test that we can load the displayCPK command to Application"""
        #from PmvApp.Pmv import MolApp
        #app = MolApp()
        app = self.app
        app.lazyLoad('displayCmds', commands=['displayCPK', 'undisplayCPK'], package='PmvApp')
        for key in ['displayCPK', 'undisplayCPK']:
            self.assertTrue(hasattr(app, key))
            cmd = getattr(app, key)
            self.assertTrue(isinstance(cmd, CmdLoader))
            cmd.loadCommand()
            self.assertTrue(key in app.commands)

    def test_002_display_cpk(self):
       """test displayCPK"""
       # display cpk with default args
       mol = self.app.readMolecule("Data/1crn.pdb")[0]
       if 'lines' not in mol.geomContainer.geoms:
           # this is done so that the atoms.colors dictionary
           # gets 'lines' key and other geometries are colored by
           # lines color by default
           self.app.lazyLoad('displayCmds', commands=['displayLines',], package='PmvApp')
           self.app.displayLines(mol)
           
       self.app.displayCPK(mol)
       geom = mol.geomContainer.geoms['cpk']
       self.assertTrue(len(geom.vertexSet) == len(mol.allAtoms))
       # test keyword args:
       # only
       sel = mol.chains.residues[:5]
       nAllatms = len(mol.allAtoms)
       nSelatms = len(sel.atoms)
       self.app.displayCPK(sel, only=True)
       self.assertTrue(len(geom.vertexSet) == nSelatms)
       
       # negate
       self.app.displayCPK(mol, negate=1) # this should set visible to 0 
       self.assertTrue(geom.visible == 0)
       self.app.displayCPK(mol, negate=0)  # display it again 
       self.assertTrue(geom.visible == 1)
       self.assertTrue(len(geom.vertexSet) == nAllatms)
       self.app.displayCPK(sel, negate=True) # undisplay atoms in sel
       self.assertTrue(geom.visible == 1)
       self.assertTrue(len(geom.vertexSet) == (nAllatms-nSelatms))
       
       # test undo
       #self.app.NEWundo() #this should display the whole mol
       #self.assertTrue(len(geom.vertexSet) == nAllatms)
       
       # scaleFactor, cpkRad , quality,  propertyName, propertyLevel
       origQual = geom.quality
       sc = 0.1
       offset = 0.2
       propvalues = mol.allAtoms.temperatureFactor
       self.app.displayCPK(mol, scaleFactor=sc, only=False, cpkRad=offset, quality=3, 
                           byproperty=True, propertyName='temperatureFactor',
                           propertyLevel = 'Atom')
       self.assertTrue(len(geom.vertexSet) == nAllatms)
       import numpy
       # the new radii by property should be:  
       radii = offset + sc*numpy.array(propvalues, "f")
       # the spheres radii:
       sphRadii = geom.vertexSet.radii.array
       sphRadii.shape=(nAllatms,)
       # the above 2 arrays should be the same:
       numpy.testing.assert_almost_equal(radii, sphRadii, 6)
       # setScale (is True by default - atm.cpkRad and atm.scaleFactor should be set)
       radarr = numpy.array([offset] * nAllatms)
       numpy.testing.assert_almost_equal(radarr, numpy.array(mol.allAtoms.cpkRad))
       scarr = numpy.array([sc] * nAllatms)
       numpy.testing.assert_almost_equal(scarr, numpy.array(mol.allAtoms.cpkScale))
       self.assertTrue(geom.quality == 3)
       
       # test undo
       #self.app.NEWundo()
       # quality goes bach to the orig value:
       #self.assertTrue(geom.quality == origQual)
       # spheres radii == atoms.radius:
       #sphRadii = geom.vertexSet.radii.array
       #sphRadii.shape=(nAllatms,)
       #numpy.testing.assert_almost_equal(numpy.array(mol.allAtoms.radius), sphRadii, 6)
       # atoms.cpkRad and atms.cpkScale are set to the default values:
       #self.assertTrue(sum(mol.allAtoms.cpkRad) == 0.0)
       #self.assertTrue(max(mol.allAtoms.cpkScale) == min(mol.allAtoms.cpkScale) == 1.0)
       
       # test error  in property value:
       
       tf = mol.allAtoms[2].temperatureFactor
       del(mol.allAtoms[2].temperatureFactor)
       self.app.displayCPK(mol, scaleFactor=sc, only=False, cpkRad=offset,
                           byproperty=True, propertyName='temperatureFactor',
                           propertyLevel = 'Atom')
       self.assertTrue(self.app._executionReport.getErrors()[0].msg == 'Error while displaying CPK for molecule %s'%mol.name)
       mol.allAtoms[2].temperatureFactor = tf
       # unitedRadii


    def test_003_display_cpk(self):
       
        """test displayCPK - invalid arguments"""
        mol = self.app.Mols[0]
        #import pdb;pdb.set_trace()
        # negate
        self.app.trapExceptions = False
        with self.assertRaises(AssertionError):
            self.app.displayCPK(mol, negate=5)
        # scaleFactor
        with self.assertRaises(AssertionError): 
            self.app.displayCPK(mol, scaleFactor="two")
        # cpkRad
        with self.assertRaises(AssertionError): 
            self.app.displayCPK(mol, cpkRad="one")          
        # quality
        with self.assertRaises(AssertionError): 
            self.app.displayCPK(mol, quality=1.5)
        # propertyName,
        with self.assertRaises(AssertionError): 
            self.app.displayCPK(mol, propertyName=1)
        with self.assertRaises(AssertionError): 
            self.app.displayCPK(mol, propertyName=[1,2,3])
        # propertyLevel,
        with self.assertRaises(AssertionError): 
            self.app.displayCPK(mol,propertyLevel='molecule')
        # setScale
        with self.assertRaises(AssertionError): 
            self.app.displayCPK(mol, setScale=5)                   
        # unitedRadii
        with self.assertRaises(AssertionError): 
            self.app.displayCPK(mol,unitedRadii=5)


    def test_004_undisplay_cpk(self):
        mol = self.app.Mols[0]
        geom = mol.geomContainer.geoms['cpk']
        sel = mol.chains.residues[:5]
        nAllatms = len(mol.allAtoms)
        nSelatms = len(sel.atoms)
        self.app.displayCPK(mol)
        self.assertTrue(len(geom.vertexSet) == nAllatms)
        self.app.undisplayCPK(sel)
        self.assertTrue(len(geom.vertexSet) == nAllatms-nSelatms)
        #self.app.NEWundo()
        #self.assertTrue(len(geom.vertexSet) == nAllatms)

       

class DisplaySticksAndBalls (TestBase):
    
    def test_001_loadCommands(self):
        """test that we can load the displayS&B commands to Application"""
        #from PmvApp.Pmv import MolApp
        #app = MolApp()
        app = self.app
        app.lazyLoad('displayCmds', commands=['displaySticksAndBalls',
                    'undisplaySticksAndBalls'], package='PmvApp')
        for key in ['displaySticksAndBalls', 'undisplaySticksAndBalls']:
            self.assertTrue(hasattr(app, key))
            cmd = getattr(app, key)
            self.assertTrue(isinstance(cmd, CmdLoader))
            cmd.loadCommand()
            self.assertTrue(key in app.commands)


    def test_002_display_SB(self):
        """test displaySticksAndBalls command"""
        # display S&B with default args
        #import pdb; pdb.set_trace()
        mol = self.app.readMolecule("Data/1crn.pdb")[0]
        if 'lines' not in mol.geomContainer.geoms:
           # this is done so that the atoms.colors dictionary
           # gets 'lines' key and other geometries are colored by
           # lines color by default
           self.app.lazyLoad('displayCmds', commands=['displayLines',], package='PmvApp')
           self.app.displayLines(mol)
        nAllatms = len(mol.allAtoms)
        self.app.displaySticksAndBalls(mol)
        balls = mol.geomContainer.geoms['balls']
        self.assertTrue(len(balls.vertexSet) == nAllatms)
        sticks = mol.geomContainer.geoms['sticks']
        self.assertTrue(len(sticks.vertexSet) == nAllatms)
        # test keyword args:
        # only
        sel = mol.chains.residues[:5]
        nSelatms = len(sel.atoms)
        self.app.displaySticksAndBalls(sel, only=True)
        self.assertTrue(len(balls.vertexSet) == nSelatms)
        self.assertTrue(len(sticks.vertexSet) == nSelatms)

        # Licorice, S&B quality, rad
        self.app.displaySticksAndBalls(mol, bRad=0.5,
                                      bquality=0, cradius=0.4, cquality=2,
                                      sticksBallsLicorice='Licorice')
        # balls quality and radii should be the same as cylinder's:
        self.assertTrue(balls.quality == sticks.quality == 2)
        n = len(balls.vertexSet.radii.array)
        balls.vertexSet.radii.array.shape = (n,)
        self.assertTrue(min(balls.vertexSet.radii.array) == max(balls.vertexSet.radii.array))
        self.assertTrue(min(sticks.vertexSet.radii.array) == max(sticks.vertexSet.radii.array))
        self.assertAlmostEqual(balls.vertexSet.radii.array[0], sticks.vertexSet.radii.array[0])
        self.app.displaySticksAndBalls(mol, bRad=0.5,
                                      bquality=5, cradius=0.4, cquality=2,
                                      sticksBallsLicorice='Sticks only')
        # balls should not be visible:
        self.assertTrue(balls.visible == 0)
        #self.app.NEWundo()
        #self.assertTrue(balls.visible == 1)
        self.app.displaySticksAndBalls(mol, bRad=0.5,
                                      bquality=5, cradius=0.4, cquality=4,
                                      sticksBallsLicorice='Sticks and Balls')
        # balls quality and radii should NOT be the same as cylinder's:
        self.assertTrue(balls.quality == 5)
        self.assertTrue(sticks.quality == 4)
        balls.vertexSet.radii.array.shape = (n,)
        self.assertTrue(min(balls.vertexSet.radii.array) == max(balls.vertexSet.radii.array))
        self.assertTrue(min(sticks.vertexSet.radii.array) == max(sticks.vertexSet.radii.array))
        self.assertAlmostEqual(balls.vertexSet.radii.array[0], 0.5)
        self.assertAlmostEqual(sticks.vertexSet.radii.array[0], 0.4)
                                     
        # negate
        self.app.displaySticksAndBalls(mol, negate=1) # this should set visible to 0 
        self.assertTrue(balls.visible == 0)
        self.assertTrue(sticks.visible == 0)       
        self.app.displaySticksAndBalls(mol, negate=0)  # display it again 
        self.assertTrue(balls.visible == 1)
        self.assertTrue(sticks.visible == 1)       
        self.assertTrue(len(balls.vertexSet) == nAllatms)
        self.app.displaySticksAndBalls(sel, negate=True) # undisplay atoms in sel
        self.assertTrue(balls.visible == 1)
        self.assertTrue(sticks.visible == 1)              
        self.assertTrue(len(balls.vertexSet) == (nAllatms-nSelatms))
        self.assertTrue(len(sticks.vertexSet) == (nAllatms-nSelatms))
        
        #
        # test undo
        #self.app.NEWundo() #this should display the whole mol
        #self.assertTrue(len(balls.vertexSet) == nAllatms)
        #self.assertTrue(len(sticks.vertexSet) == nAllatms)


    def test_003_display_SB(self):
        """test displaySticksAndBalls - not valid arguments"""
        
        mol = self.app.Mols[0]
        self.app.trapExceptions = False
        with self.assertRaises(AssertionError):
            #only
            self.app.displaySticksAndBalls(mol, only=None)
        with self.assertRaises(AssertionError):
            #negate
            self.app.displaySticksAndBalls(mol, negate=None)
        import numpy
        with self.assertRaises(AssertionError):
            #bRad
            self.app.displaySticksAndBalls(mol, bRad=numpy.array([1,1,1]))        
        with self.assertRaises(AssertionError):
            #bScale
            self.app.displaySticksAndBalls(mol, bScale="one")
        with self.assertRaises(AssertionError):
            #bquality
            self.app.displaySticksAndBalls(mol, bquality=0.3)
        with self.assertRaises(AssertionError):
            self.app.displaySticksAndBalls(mol, bquality=-1)
        with self.assertRaises(AssertionError):
            #cradius
            self.app.displaySticksAndBalls(mol, cradius=numpy.array([1,1,1]))
        with self.assertRaises(AssertionError):
            #cquality
            self.app.displaySticksAndBalls(mol, cquality='one')
        with self.assertRaises(AssertionError):
            #sticksBallsLicorice
            self.app.displaySticksAndBalls(mol, sticksBallsLicorice="Sticks, Balls")
        with self.assertRaises(AssertionError):
            #setScale
            self.app.displaySticksAndBalls(mol, setScale=5)


    def test_004_undisplay_SB(self):
        crn = self.app.Mols[0]
        ins = self.app.readMolecule('Data/7ins.pdb')
        if 'lines' not in ins[0].geomContainer.geoms:
           # this is done so that the atoms.colors dictionary
           # gets 'lines' key and other geometries are colored by
           # lines color by default
           self.app.lazyLoad('displayCmds', commands=['displayLines',], package='PmvApp')
           self.app.displayLines(ins)
        nall = len(ins.allAtoms)
        nchain = len(ins.chains[0].residues.atoms)
        self.app.displaySticksAndBalls(ins)
        balls = ins[0].geomContainer.geoms['balls']
        sticks = ins[0].geomContainer.geoms['sticks']
        self.assertTrue(len(balls.vertexSet) == nall)
        self.assertTrue(len(sticks.vertexSet) == nall)
        # undisplay S&B for one chain
        self.app.undisplaySticksAndBalls(ins.chains[0])
        self.assertTrue(len(balls.vertexSet) == nall-nchain)
        self.assertTrue(len(sticks.vertexSet) == nall-nchain)
        # undo - show S&B for the whole molecule
        #self.app.NEWundo()
        #self.assertTrue(len(balls.vertexSet) == nall)
        #self.assertTrue(len(sticks.vertexSet) == nall)
        #self.app.undisplaySticksAndBalls(crn)
        # 1crn should be invisible:
        #self.assertTrue(crn.geomContainer.geoms['balls'].visible == 0)
        #self.assertTrue(crn.geomContainer.geoms['sticks'].visible == 0)
        # 7ins is visible:
        #self.assertTrue(balls.visible == 1)
        #self.assertTrue(sticks.visible == 1)
        #self.app.NEWundo()
        # should show 1crn
        #self.assertTrue(crn.geomContainer.geoms['balls'].visible == 1)
        #self.assertTrue(crn.geomContainer.geoms['sticks'].visible == 1)


class DisplayBackboneTrace(TestBase):
    
    def test_001_loadCommands(self):
        """test that we can load the displayBackboneTrace commands to Application"""
        #from PmvApp.Pmv import MolApp
        #app = MolApp()
        app = self.app
        app.lazyLoad('displayCmds', commands=['displayBackboneTrace', 'undisplayBackboneTrace'], package='PmvApp')
        for key in ['displayBackboneTrace', 'undisplayBackboneTrace']:
            self.assertTrue(hasattr(app, key))
            cmd = getattr(app, key)
            self.assertTrue(isinstance(cmd, CmdLoader))
            cmd.loadCommand()
            self.assertTrue(key in app.commands)


    def test_002_display_BackboneTrace(self):
        mol=self.app.readMolecule("Data/test_barrel_1_2_hbonds.pdb")
        # test displayBackboneTrace command : default args
        caAtms = [a for a in mol.allAtoms if a.name =='CA']
        if not hasattr (self.app, "displayLines"):
            self.app.lazyLoad("displayCmds", commands=["displayLines"], package="PmvApp")
        self.app.displayLines(mol)
        self.app.displayBackboneTrace(mol)
        caBalls = mol[0].geomContainer.geoms['CAballs']
        caSticks = mol[0].geomContainer.geoms['CAsticks']
        self.assertTrue(len(caBalls.vertexSet) == len(caAtms))
        self.assertTrue(len(caSticks.vertexSet) == len(caAtms))
        # only
        ats = mol.chains[0].getAtoms()
        natms = len([a for a in ats if a.name =='CA'])
        #print "len CA atoms in ", ats, natms
        self.app.displayBackboneTrace(ats, only=True,cradius=0.5, cquality=2 )
        self.assertTrue(len(caBalls.vertexSet) == natms)
        self.assertTrue(len(caSticks.vertexSet) == natms)
        # balls quality and radii should be the same as cylinder's:
        self.assertTrue(caBalls.quality == caSticks.quality == 2)
        n = len(caBalls.vertexSet.radii.array)
        caBalls.vertexSet.radii.array.shape = (n,)
        self.assertTrue(min(caBalls.vertexSet.radii.array) == max(caBalls.vertexSet.radii.array))
        self.assertTrue(min(caSticks.vertexSet.radii.array) == max(caSticks.vertexSet.radii.array))
        self.assertAlmostEqual(caBalls.vertexSet.radii.array[0], caSticks.vertexSet.radii.array[0])
        #self.app.NEWundo()
        #self.assertTrue(caBalls.quality == caSticks.quality == 5)
        #self.assertTrue(len(caBalls.vertexSet) == len(caAtms))
        #self.assertTrue(len(caSticks.vertexSet) == len(caAtms))
        #negate
        self.app.displayBackboneTrace(ats, negate=True)
        self.assertTrue(len(caBalls.vertexSet) == len(caAtms)-natms)
        self.assertTrue(len(caSticks.vertexSet) == len(caAtms)-natms)
        # sticksBallsLicorice='Sticks and Balls'
        self.app.displayBackboneTrace(mol, bRad=0.5,
                                     bquality=5, cradius=0.4, cquality=2,
                                     sticksBallsLicorice='Sticks and Balls')
        self.assertTrue(len(caBalls.vertexSet) == len(caAtms))
        self.assertTrue(len(caSticks.vertexSet) == len(caAtms))
        self.assertTrue(caBalls.quality == 5)
        self.assertTrue(caSticks.quality == 2)
        n = len(caBalls.vertexSet.radii.array)
        caBalls.vertexSet.radii.array.shape = (n,)
        self.assertTrue(min(caBalls.vertexSet.radii.array) == max(caBalls.vertexSet.radii.array))
        self.assertTrue(min(caSticks.vertexSet.radii.array) == max(caSticks.vertexSet.radii.array))
        self.assertAlmostEqual(caBalls.vertexSet.radii.array[0], 0.5)
        self.assertAlmostEqual(caSticks.vertexSet.radii.array[0], 0.4)


    def test_003_loadCommands(self):
        """test that we can load the displayBackboneTrace commands to Application"""
        #from PmvApp.Pmv import MolApp
        #app = MolApp()
        app = self.app
        app.lazyLoad('displayCmds', package='PmvApp')
        for key in ['displayBoundGeom',
                    'undisplayBoundGeom','bindGeomToMolecularFragment',
                    'showMolecules']:
            self.assertTrue(hasattr(app, key))
            cmd = getattr(app, key)
            self.assertTrue(isinstance(cmd, CmdLoader))
            cmd.loadCommand()
            self.assertTrue(key in app.commands)
       

if __name__ == '__main__':
    import os
    os.chdir(os.path.split(testBase.__file__)[0])

    unittest.main()
