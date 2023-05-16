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

"""This file tests some basic features of the Pvv package such as:
   - loading the available commands;
   - loading and displaying a volume;
   - adding a volume bounding bbox;
   - saving lookup table (LUT) in a file;
   - restoring LUT from the file;
   - splitting the LUT widget;
   - cropping the volume;
   - scaling and translating the volume object;


"""
import numpy
from mglutil.regression import testplus
from Pmv.moleculeViewer import MoleculeViewer
import traceback
import sys
import time
mv = None
from . import basicPvv

def setUpSuite():
    """Create a Molecule Viewer."""
    
    global mv
    mv = MoleculeViewer(logMode = 'no', withShell=0)
    mv.setUserPreference(('trapExceptions', '0'), log = 0)
    # Redirect the standard error output which is in pmv the pyshell to
    # the terminal.
    oldstderr = sys.stderr
    sys.stderr = sys.__stderr__
    mv.loadModule('dejaVuCommands', 'ViewerFramework')
    #basicPvv.loadModules(mv, "vli")
    loadModules()
    readDataFile()
    writeLUT()

def tearDownSuite():
    """Quit the viewer."""
    
    mv.Exit(0)


def loadModules():
    """ Load loadPvvCommands module and test its __call__() method
    that tries to import the volume rendering libraries and loads all
    available Pvv commands."""
    from Volume.Renderers import setvals
    setvals(1, "vli")
    from Volume.Pvv import volGeom
    if volGeom:
        if volGeom.name != "vli":
            from Volume.Pvv import initModules
            initModules("vli")

    basicPvv.loadModules(mv, "vli")
    

def readDataFile():
    """ Tests vvCommands __call__() method.
    Read data file and display the volume. """
    
    basicPvv.readDataFile(mv, "vli")



def writeLUT():
    """Create LUT data and write it in a file."""

    basicPvv.writeLUT(mv, "vli")

def test_01readLUT():
    """Tests transferCommands __call__() method.
    Load LUT from a file."""

    basicPvv.readLUT(mv, "vli")
    
def test_02splitLUT():
    """Tests transferCommands __call__() method.
    Splits/unsplits the LUT widget. """
    
    basicPvv.splitLUT(mv, "vli")

def test_03addBoundingBox():
    """ Tests boundingboxCommands __call__() method.
    Adds a volume object's bounding box. """
    
    basicPvv.addBoundingBox(mv, "vli")

def test_04crop():
    """ Tests cropCommands __call__() method.
    Crop the volume object."""

    basicPvv.Crop(mv, "vli")

def test_05transformVolume():
    """Tests voltransformCommans __call__() method.
    It scales or translates the volume object. """
    
    basicPvv.transformVolume(mv, "vli")

def test_06gradOpacity():
    mv.VLIOptions(opacity= 1)
    for i in range(10):
        mv.rotateScene(nbSteps=1) 
    mv.VLIOptions( opacity = 0)

def test_07blendMode():
    mv.VLIOptions(minIntensity = 1)
    for i in range(10):
        mv.rotateScene(nbSteps=1)
    mv.VLIOptions(maxIntensity = 1)
    for i in range(10):
        mv.rotateScene(nbSteps=1)
    mv.VLIOptions(frontToBack = 1)


def test_08materialProperties():
    vals = (numpy.array([list(range(1,10,1)),list(range(10,1,-1))])*0.1).ravel()
    props = {'d':0.2, 's':0.2, 'e':0.2, 'se':0.1}
    for prop in list(props.keys()):
        for val in vals:
            props[prop] = val
            #print "mat. prop: ", props
            mv.VLIOptions(matProp = (props['d'], props['s'],
                                     props['e'], props['se']*10))
    from Volume.Pvv import volGeom
    assert volGeom
    mp = volGeom.context.GetReflectionProperties()
    print("mp:", mp)
    mv.VLIOptions(matProp = (0.3, 0.4, 0.2, 8.0))
    mp = volGeom.context.GetReflectionProperties()
    assert mp == (0.3, 0.4, 0.2, 8.0)


def test_09superSampling():
    for x in (1,2,3):
        for y in (1,2,3):
            for z in (1,2,4):
                mv.VLIOptions(sampling = (x,y,z))
    from Volume.Pvv import volGeom
    assert volGeom
    ss = volGeom.context.GetSuperSamplingFactor()
    print("ss:", ss)
    assert ss[0]*3 == 1
    assert ss[1]*3 == 1
    assert ss[2]*4 == 1
    
    mv.VLIOptions(sampling = (1,1,1))
    ss = volGeom.context.GetSuperSamplingFactor()
    print("ss:", ss)
    assert ss == (1,1,1)

def test_10light1():
    from Volume.Pvv import volGeom
    assert volGeom
    d =volGeom.currLight.GetDirection()
    ldir = (d[0],d[1],d[2])
    vals=numpy.array([list(range(-10, 1)),list(range(11))])*.1
    vals = vals.ravel().tolist()
    x = -1
    for x in vals:
        mv.VLILight(direction = (x, -1.0, -1.0))
    vals.reverse()
    for x in vals:
        mv.VLILight(direction = (x, -1.0, 1.0))
    d =volGeom.currLight.GetDirection()
    ldir1 = (d[0],d[1],d[2])
    print("ldir: ", ldir, ldir1)
    assert ldir[2] != ldir1[2]

def test_11light2():
    mv.VLILight(select = 2)
    mv.VLILight(switch = 'on')
    from Volume.Pvv import volGeom
    mv.VLILight(switch = 'off')
    nlights = volGeom.context.GetLightCount()
    print("nlights=", nlights)
    assert nlights == 1
    mv.VLILight(switch = 'on')
    nlights = volGeom.context.GetLightCount()
    print("nlights=", nlights)
    assert nlights == 2
    vals=numpy.array([list(range(-10, 1)),list(range(11))])*.1
    vals = vals.ravel().tolist()
    mv.VLILight(direction = (vals[0], -1.0, -1.0))
    d =volGeom.currLight.GetDirection()
    dir1 = (d[0],d[1],d[2])
    for x in vals:
        mv.VLILight(direction = (x, -1.0, -1.0))
    d =volGeom.currLight.GetDirection()
    dir2 = (d[0],d[1],d[2])
    assert dir1[0] != dir2[0]


if __name__ == '__main__':
    #print sys.argv
    
    testplus.chdir()
    args = ()
    if len( sys.argv) > 1:
        args = (sys.argv[1],)
    harness = testplus.TestHarness( __name__,
                                connect = (setUpSuite, args, {}) ,
                                funs = testplus.testcollect( globals()),
                                disconnect = tearDownSuite
                                )
    print(harness)
    sys.exit( len( harness))






