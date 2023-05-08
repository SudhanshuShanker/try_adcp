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
#from mglutil.regression import testplus
from Pmv.moleculeViewer import MoleculeViewer
import traceback
import sys
import time
mv = None
from . import basicPvv

def setUpSuite():
    """Create a Molecule Viewer."""
    from Volume.Renderers.UTVolumeLibrary import UTVolumeLibrary
    from Volume.Renderers.UTVolumeLibrary.DejaVu.UTVolRenGeom import UTVolRenGeom
    global mv
    mv = MoleculeViewer(logMode = 'no', withShell=0)
    mv.setUserPreference(('trapExceptions', '0'), log = 0)
    # Redirect the standard error output which is in pmv the pyshell to
    # the terminal.
    oldstderr = sys.stderr
    sys.stderr = sys.__stderr__
    mv.loadModule('dejaVuCommands', 'ViewerFramework')
    basicPvv.loadModules(mv, "utvolren")
    readDataFile()
    writeLUT()

def tearDownSuite():
    """Quit the viewer."""
    
    mv.Exit(0)


##  def test_loadModules():
##      """ Load loadPvvCommands module and test its __call__() method
##      that tries to import the volume rendering libraries and loads all
##      available Pvv commands."""

##      basicPvv.loadModules(mv, "utvolren")

def readDataFile():
    """ Tests vvCommands __call__() method.
    Read data file and display the volume. """
    
    basicPvv.readDataFile(mv, "utvolren")

def test_1addBoundingBox():
    """ Tests boundingboxCommands __call__() method.
    Adds a volume object's bounding box. """
    
    basicPvv.addBoundingBox(mv, "utvolren")

def writeLUT():
    """Create LUT data and write it in a file."""

    basicPvv.writeLUT(mv, "utvolren")

def test_2readLUT():
    """Tests transferCommands __call__() method.
    Load LUT from a file."""

    basicPvv.readLUT(mv, "utvolren")
    
def test_3splitLUT():
    """Tests transferCommands __call__() method.
    Splits/unsplits the LUT widget. """
    
    basicPvv.splitLUT(mv, "utvolren")

def test_4Crop():
    """ Tests cropCommands __call__() method.
    Crop the volume object."""

    basicPvv.Crop(mv, "utvolren")

def test_5transformVolume():
    """Tests voltransformCommans __call__() method.
    It scales or translates the volume object. """
    
    basicPvv.transformVolume(mv, "utvolren")


## if __name__ == '__main__':
##     #print sys.argv
    
##     testplus.chdir()
##     args = ()
##     if len( sys.argv) > 1:
##         args = (sys.argv[1],)
##     harness = testplus.TestHarness( __name__,
##                                 connect = (setUpSuite, args, {}) ,
##                                 funs = testplus.testcollect( globals()),
##                                 disconnect = tearDownSuite
##                                 )
##     print harness
##     sys.exit( len( harness))






