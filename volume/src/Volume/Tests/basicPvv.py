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
import traceback
import sys
import time

def loadModules(mv, libName):
    """ Load loadPvvCommands module and test its __call__() method
    that tries to import the volume rendering libraries and loads all
    available Pvv commands."""
    from Volume.Renderers import setvals
    setvals(1, libName)
    try:
        mv.loadModule("loadAllCommands", "Volume.Pvv")
    except:
        print("\n\nLOADERROR:%s\n"%( 'loadPvvCommands'))
        traceback.print_exc(file=sys.stdout)

    from Volume.Pvv import volGeom
#    if not volGeom:
#        print "no volGeom created.."
#        sys.exit()
    print("volGeom:" , volGeom)
    print("libName:", libName)
    assert  libName == volGeom.name, ("%s, %s\n"%(libName, volGeom))
    try:
        mv.LoadAll()
    except:
        print("\n\nLoadAll()ERROR\n")
        traceback.print_exc(file=sys.stdout)




def readDataFile(mv, libName):
    """ Tests vvCommands __call__() method.
    Read data file and display the volume. """
    
    if libName == 'vli':
        mv.StartVLI("Data/xaa.aypyd.vox")
    elif libName == 'utvolren':
        mv.StartUTVolRen("Data/ct_head.rawiv")
        vi=mv.GUI.VIEWER
        root=vi.rootObject
        #root.SetScale((8.,8.,8.))
        mv.rotateScene(stepSize=90, axis=(1,0,0), nbSteps=1)
        mv.rotateScene(stepSize=180, nbSteps=1)

def addBoundingBox(mv, libName):
    """ Tests boundingboxCommands __call__() method.
    Adds a volume object's bounding box. """
    
    if libName == 'vli':
        mv.VLIBoundBox()
    elif libName == 'utvolren':
        mv.UTBoundBox()

def writeLUT(mv, libName):
    """Create LUT data and write it in a file."""

    # Create data to save in a file.
    # There is no method in Pvv/transferCommands.py to set LUT -
    # only through GUI (the module's __call__() sets LUT saved previously
    # in a file) .
    if libName == 'vli':
        com = mv.VLITransfer
        com.tm.intervals_list = [(0, 255)]
        lut = com.tm.lut_list[0]
        lut.shapes = [0, 1, 7, 8, 10, 11]
        colors = (numpy.array( [[255, 255, 255],[255, 255, 255],
                                  [0, 204, 51], [16, 140, 31],
                                  [37, 216, 51], [86, 92, 165],
                                  [68, 99, 242], [74, 96, 255],
                                  [0, 0, 0], [127, 45, 16],
                                  [255, 0, 23]], 'f')/255.0).astype('f')
        alphas = [0, 0, 1873, 964,  132, 0, 1293, 0, 0, 4021, 4080, 4080]
        values = [0, 58, 62, 74, 85, 94, 103, 107, 245, 246, 255, 255]
        #lut.points = computeLUTpoints(lut, values, alphas)
        savefile = "Data/test_vli.lut"
    elif libName == 'utvolren':
        com = mv.UTVolRenTransfer
        com.tm.intervals_list = [(0, 255)]
        lut = com.tm.lut_list[0]
        lut.shapes=[0, 1, 5, 6]
        values=[0, 64, 70, 112, 150, 151, 255]
        alphas=[0, 0, 109, 126, 100, 0, 0]
        colors= [[1.0, 1.0, 1.0], [0.5, 0.0, 0.0], [0.5, 0.5, 0.5], [1.0, 1.0, 1.0],
                 [0.4, 0.4, 0.4], [0.4, 0.4, 0.4], [1.0, 1.0, 1.0]]
        #lut.points = computeLUTpoints(lut, values, alphas)
        savefile = "Data/test_utvolren.lut"
    lut.color_arr=numpy.zeros((256, 3), 'f')
    lut.color_arr[values[0]] = colors[0]
    lut.color_arr[values[-1]]= colors[-1]
    lut.last_event ='ButtonRelease-1'
    lut.curr_ind = 0
    for i in range(len(values)-2):
        lut.set_colors(colors[i+1], values[i], values[i+1], values[i+2])
    #print lut.color_arr
    lut.xminval = 0
    lut.values = values
    lut.alpha_arr = numpy.zeros(256, 'i')
    for i in range(len(values)):
        lut.alpha_arr[values[i]] = alphas[i]
    com.tm.saveLUT(file=savefile)
    import time
    #time.sleep(1)

def computeLUTpoints(lut, values, alphas):
    points = [(lut.left, lut.bott)] 
    for i in range(len(values)):
        points.append(((values[i]-lut.xminval)*lut.sclx+lut.left,
                           lut.bott-lut.scly*alphas[i]))
    points.append((lut.right, lut.bott))
    print("points: ", points)
    return points



def readLUT(mv, libName):
    """Tests transferCommands __call__() method.
    Load LUT from a file."""
    
    if libName == 'vli':
        com = mv.VLITransfer
        openfile = "Data/test_vli.lut"
    elif libName == "utvolren":
        com = mv.UTVolRenTransfer
        openfile = "Data/test_utvolren.lut"
    #com.tm.reset()
    #com.guiCallback()
    com(openfile)
    for i in range(20):
	mv.rotateScene(nbSteps=1)

def splitLUT(mv, libName):
    """Tests transferCommands __call__() method.
    Splits/unsplits the LUT widget. """
    
    if libName == 'vli':
        com = mv.VLITransfer
    elif libName == "utvolren":
        com = mv.UTVolRenTransfer
    com.guiCallback()
    for i in range(8):
	mv.rotateScene(nbSteps=1)
    com(50, 100, split = 1)
    intervals = com.tm.intervals_list
    assert len(intervals) == 3
    assert intervals[0] == (0, 49)
    assert intervals[1] == (50, 100)
    assert intervals[2] == (101, 255)
    #print "intervals: ", com.tm.intervals_list
    for i in range(8):
	mv.rotateScene(nbSteps=1)
    com(50, 100, split = 0)
    intervals = com.tm.intervals_list
    #print "intervals: ", com.tm.intervals_list
    assert len(intervals) == 1
    assert intervals[0] == (0, 255)
    for i in range(8):
	mv.rotateScene(nbSteps=1)
    com.destroy()

def Crop(mv, libName):
    """ Tests cropCommands __call__() method.
    Crop the volume object."""
    
    com = mv.CropCommand
    from Volume.Pvv import volGeom
    if volGeom:
        crop = volGeom.cropBox.crop
        list1=[]
        i=0
        while i < 32:
            list1.append( (i+2, 64-i))
            i=i+2
        for l in list1:
            com(SlabX = l, log = 0)
            com(SlabY = l, log = 0)
            com(SlabZ = l, log = 0)
            if libName == 'vli':
                sl = crop.GetSlabs() # VLI function
                assert (sl[0], sl[1]) == l
        list1.reverse()
        for l in list1:
            com(SlabX = l, log = 0)
            com(SlabY = l, log = 0)
            com(SlabZ = l, log = 0)
            if libName == 'vli':
                sl = crop.GetSlabs() # VLI function
                assert (sl[0], sl[1]) == l
    else:
        print("in test_Crop(): volGeom is None")

def transformVolume(mv, libName):
    """Tests voltransformCommans __call__() method.
    It scales or translates the volume object. """
    from Volume.Pvv import volGeom
    if not volGeom:
       print("in test_transformVolume() : volGeom is None, libName=", libName)
    assert volGeom
    if libName == 'vli':
        com = mv.VLITransformation
    elif libName == 'utvolren':
        com = mv.UTVolRenTransformation
    sc = (1, 1, 1)
    tr = (0,0,0)
    for i in range(5):
        newsc = (sc[0]+0.2, sc[1]+0.2, sc[2]+0.2)
        com(scale = newsc)
        sc = newsc
    if libName == 'vli':
        scaleMat = volGeom.vliScalemat
        scale = (str(scaleMat[0][0]) , str(scaleMat[1][1]),
                 str(scaleMat[2][2]) )
    elif libName == 'utvolren':
        scaleMat = volGeom.scale
        scale = (str(scaleMat[0]) , str(scaleMat[1]),
                 str(scaleMat[2]) )
        #print "scale: ", scale
    assert scale == (str(2.0), str(2.0), str(2.0) )

    for i in range(5):
        newsc = (sc[0]-0.2, sc[1]-0.2, sc[2]-0.2)
        com(scale = newsc)
        sc = newsc
    if libName == 'vli':
        scaleMat = volGeom.vliScalemat
        scale = (str(scaleMat[0][0]), str(scaleMat[1][1]),
                 str(scaleMat[2][2]))
    elif libName == 'utvolren':
        scaleMat = volGeom.scale
        scale = (str(scaleMat[0]) , str(scaleMat[1]),
                 str(scaleMat[2]) )
    assert scale == (str(1.0), str(1.0), str(1.0) )
        #print "scale: ", scale
    for i in range(5):
        newtr = (tr[0]+1., tr[1]+1., tr[2]+1.)
        com(translate = newtr)
        tr = newtr
    if libName == 'vli':
        transMat = volGeom.vliTranslate
        trans = (str(transMat[0][3]), str(transMat[1][3]),
                 str(transMat[2][3]) )
        
    elif libName == 'utvolren':
        transMat = volGeom.translation
        trans = (str(transMat[0]), str(transMat[1]),
                 str(transMat[2]) )
    #print "trans: ", trans
    assert trans == (str(5.0), str(5.0), str(5.0))
    for i in range(5):
        newtr = (tr[0]-1., tr[1]-1., tr[2]-1.)
        com(translate = newtr)
        tr = newtr
    if libName == 'vli':
        transMat = volGeom.vliTranslate
        trans = (transMat[0][3], transMat[1][3],
                 transMat[2][3] )
    elif libName == 'utvolren':
        transMat = volGeom.translation
        trans = (transMat[0], transMat[1],
                 transMat[2] )
    #print "trans: ", trans
    assert trans ==(0.0, 0.0, 0.0 )






