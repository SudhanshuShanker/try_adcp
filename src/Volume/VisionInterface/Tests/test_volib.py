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

#########################################################################
#
# Date: Aug 2003  Authors: Daniel Stoffler, Michel Sanner
#
#       stoffler@scripps.edu
#       sanner@scripps.edu
#
# Copyright: Daniel Stoffler, Michel Sanner, and TSRI
#
#########################################################################

import sys
ed = None

def setUp():
    global ed
    from Vision.VPE import VisualProgramingEnvironment
    ed = VisualProgramingEnvironment(name='Vision', withShell=0,)
    ed.master.update_idletasks()
    ed.configure(withThreads=0)


def tearDown():
    ed.exit_cb()
    import gc
    gc.collect()

##########################
## Helper methods
##########################

def pause(sleepTime=0.1):
    from time import sleep
    ed.master.update()
    sleep(sleepTime)

##########################
## Tests
##########################

def test_01_loadStandardLib():
    from Volume.VisionInterface.VolumeNodes import vollib
    ed.addLibraryInstance(vollib, 'Volume.VisionInterface.VolumeNodes', 'vollib')
    ed.master.update_idletasks()
    pause()

def categoryTest(cat): 
    # test all nodes in given category by adding them to the canvas,
    #show widgets in node if available and show paramPanel if available,
    #then delete node.
    test_01_loadStandardLib()
    lib = 'volume'
    libs = ed.libraries
    posx = 150
    posy = 150

    for node in libs[lib].libraryDescr[cat]['nodes']:
        klass = node.nodeClass
        kw = node.kw
        args = node.args
        netNode = klass(*args, **kw)
        print('testing: '+node.name) # begin node test
        #add node to canvas
        ed.currentNetwork.addNode(netNode,posx,posy)
        # show widget in node if available:
        widgetsInNode = netNode.getWidgetsForMaster('Node')
        if len( list(widgetsInNode.items()) ):
            if not netNode.isExpanded():
                netNode.toggleNodeExpand_cb()
                ed.master.update_idletasks()
                pause()
            else:
                pause()
            # and then hide it
            netNode.toggleNodeExpand_cb()
            ed.master.update_idletasks()
            pause()

        # show widgets in param panel if available:
        widgetsInPanel = netNode.getWidgetsForMaster('ParamPanel')
        if len(list(widgetsInPanel.items())):
            netNode.paramPanel.show()
            ed.master.update_idletasks()
            pause()
            #and then hide it
            netNode.paramPanel.hide()
            ed.master.update_idletasks()

        # and now delete the node
        ed.currentNetwork.deleteNodes([netNode])
        ed.master.update_idletasks()
        print('passed: '+node.name) # end node test
        
categories = ['Mapper', 'Operator', 'Filter', 'Macro', 'Input', 'Output']

def test_02_FilterCategory():
    categoryTest("Filter")

def test_03_InputCategory():
    categoryTest("Input")
    
def test_04_MacrosCategory():
    categoryTest("Macro")
    
def test_05_MapperCategory():
    categoryTest("Mapper")

def test_06_OperatorsCategory():
    categoryTest("Operator")

def test_07_Outputcategory():
    categoryTest("Output")
    
