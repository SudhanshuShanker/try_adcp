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

import os, sys
import time

ed = None

def setUp():
    """Set up Vision"""
    global ed
    from Vision.VPE import VisualProgramingEnvironment
    ed=VisualProgramingEnvironment(name='Vision',withShell=0,)
    ed.master.update_idletasks()
    ed.configure(withThreads=0)

def tearDown():
    """Tear down and close Vision"""
    ed.exit_cb()
    import gc
    gc.collect()

##########################
## Helper methods
##########################

def pause(sleepTime=0.15):
    ed.master.update()
    time.sleep(sleepTime)

def setUpMRCNetwork():
    """Set up the MRC read node"""
    net=ed.currentNetwork

    from Volume.VisionInterface.VolumeNodes import vollib
    from Volume.VisionInterface.VolumeNodes import ReadMRCfile
    ed.addLibraryInstance(vollib,"Volume.VisionInterface.VolumeNodes",'vollib')

    #create read and write nodes
    readNode=ReadMRCfile(constrkw={},name='ReadMRC',
                          library=vollib)

    #place nodes in vision
    net.addNode(readNode,150,150)
    
    return (readNode)

def setUpCCP4Network():
    """Set up the CCP4 read and write nodes"""
    net=ed.currentNetwork

    from Volume.VisionInterface.VolumeNodes import vollib
    from Volume.VisionInterface.VolumeNodes import ReadCCP4file
    from Volume.VisionInterface.VolumeNodes import WriteCCP4file
    from Volume.IO.volReaders import ReadCCP4
    ed.addLibraryInstance(vollib,"Volume.VisionInterface.VolumeNodes",'vollib')

    #create read and write nodes
    readNode=ReadCCP4file(constrkw={},name='ReadCCP4',
                          library=vollib)
    writeNode=WriteCCP4file(constrkw={},name='WriteCCP4',
                            library=vollib)
    #place nodes in vision
    net.addNode(readNode,150,150)
    net.addNode(writeNode,150,250)

    net.connectNodes(readNode,writeNode,"grid","grid",blocking=True)
    
    check=ReadCCP4()
    
    return (readNode,writeNode,check)

def cleanUp():
    nodes = ed.currentNetwork.nodes[:]
    allNodes = ed.currentNetwork.getAllNodes(nodes)
    ed.currentNetwork.deleteNodes(allNodes)
    for lib in list(ed.libraries.values()):
        ed.deleteLibrary(lib.name)
    pause()
    
##########################
## Tests
##########################

def test_00_readMRCfile():
    """Read an MRC file"""

    file1='Data/nwv1.mrc'
    
    reading=setUpMRCNetwork()

    #load file into node
    reading.inputPorts[0].widget.set(os.path.abspath(file1),0)
    
    readCheck=reading.run()
    assert readCheck
    pause()
    
    cleanUp()

def test_01_readWriteCCP4File():
    """
    Reads a CCP4 file, displays header data, then writes it to a new file.
    The new file is then read and checked to make sure it contains the
    same data as the original
    """

    timestamp= time.strftime("%Y%m%d%H%M%S")

    file1='Data/nwv1.map'
    fileNew='Data/tmp_%s.map'%timestamp
    reading,writing,checking=setUpCCP4Network()

    #enter file names into nodes
    reading.inputPorts[0].widget.set(os.path.abspath(file1),0)
    writing.inputPorts[0].widget.set(os.path.abspath(fileNew),0)

    #read file1
    readCheck=reading.run()
    assert readCheck

    #write new File
    writeCheck=writing.run(fileNew)
    assert writeCheck

    #read new File.
    reading.inputPorts[0].widget.set(os.path.abspath(fileNew),0)
    reReadCheck=reading.run()
    assert reReadCheck
    pause()

    #remove newly created test file
    os.remove(fileNew)
    
    cleanUp()
