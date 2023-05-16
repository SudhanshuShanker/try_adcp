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

import unittest, sys
from PmvApp.Pmv import MolApp
from numbers import Integral as INT


class CreateApp(unittest.TestCase):

    def test_001_sanityCheck(self):
        """
        tests that the App is created
        """
        app = MolApp()
        app.exit()
        assert sys.getrefcount(app)==2


    def test_002_addingMolecule(self):
        app = MolApp()
        from MolKit import Read
        mols = Read('Data/1crn.pdb')
        app.addObject('Crambin', mols[0], 'Molecule') 
        self.assertTrue(len(app.objects['Molecule'])==1)

        app.removeObject(mols[0], 'Molecule')
        self.assertTrue(len(app.objects['Molecule'])==0)
        app.exit()
        assert sys.getrefcount(app)==2


    def test_003_addingCmdCalledOnAdd1(self):
        app = MolApp()

        class cmd:
            def __init__(self, name):
                self.name = name
                self.called = False            
            def __call__(self, *args, **kw):
                print(self.name, args, kw)
                self.called = True

        cmd1 = cmd('cmd1')
        cmd2 = cmd('cmd2')

        app.setOnAddObjectCmd( 'Molecule', [cmd1, cmd2])
        from MolKit import Read
        mols = Read('Data/1crn.pdb')
        app.addObject('Crambin', mols[0], 'Molecule') 

        self.assertTrue(cmd1.called==True)
        self.assertTrue(cmd2.called==True)
        app.exit()
        assert sys.getrefcount(app)==2


    def test_004_addingCmdCalledOnAdd2(self):
        app = MolApp()

        class cmd:
            def __init__(self, name):
                self.name = name
                self.called = False            

            def __call__(self, *args, **kw):
                self.args = args
                self.kw = kw
                self.called = True

        cmd1 = cmd('cmd1')
        cmd2 = cmd('cmd2')

        argList = [ ('hello',), ()]
        kwList = [{}, {'time':'now'}]
        
        app.setOnAddObjectCmd( 'Molecule', [cmd1, cmd2], argList, kwList) 

        from MolKit import Read
        mols = Read('Data/1crn.pdb')
        app.addObject('Crambin', mols[0], 'Molecule') 

        self.assertTrue(cmd1.called==True)
        self.assertTrue(cmd1.args[0]==mols[0]) 
        self.assertTrue(cmd1.args[1]=='hello') 
        self.assertTrue(cmd2.called==True)
        self.assertTrue(cmd2.kw['time']=='now') 

        app.exit()
        assert sys.getrefcount(app)==2


    def test_005_addingMoleculeEvents(self):
        """
        tests that we can add a molecule and all the
        events are generated properly
        """
        self.calls = [False]*5

        from Molkit2.molecule import Molecule
        def startAddObject_cb(event):
            assert event.name=='Crambin'
            assert isinstance(event.object, Molecule)
            self.calls[0] = True
            
        def addObjectCmd_cb(event):
            assert isinstance(event.number, INT)
            assert isinstance(event.total, INT)
            assert isinstance(event.cmdName, str)
            self.calls[1] = True

        def endAddObject_cb(event):
            assert isinstance(event.object, Molecule)
            self.calls[2] = True
            
        def beforeDeleteObject_cb(event):
            assert isinstance(event.object, Molecule)
            self.calls[3] = True

        def afterDeleteObject_cb(event):
            assert isinstance(event.object, Molecule)
            self.calls[4] = True

        class cmd:
            def __init__(self, name):
                self.name = name
                self.called = False            

            def __call__(self, *args, **kw):
                self.called = True

        cmd1 = cmd('cmd1')
        cmd2 = cmd('cmd2')
        from PmvApp.Pmv import StartAddMoleculeEvent, AddMoleculeCmdEvent, \
             EndAddMoleculeEvent, BeforeDeleteMoleculeEvent, \
             AfterDeleteMoleculeEvent
        from mglutil.events import registerListener, unregisterListener
        registerListener(StartAddMoleculeEvent, startAddObject_cb)
        registerListener(AddMoleculeCmdEvent, addObjectCmd_cb)
        registerListener(EndAddMoleculeEvent, endAddObject_cb)
        registerListener(BeforeDeleteMoleculeEvent, beforeDeleteObject_cb)
        registerListener(AfterDeleteMoleculeEvent, afterDeleteObject_cb)

        app = MolApp()
        app.setOnAddObjectCmd( 'Molecule', [cmd1, cmd2])
        from MolKit import Read
        mols = Read('Data/1crn.pdb')
        app.addObject('Crambin', mols[0], 'Molecule') 

        unregisterListener(StartAddMoleculeEvent, startAddObject_cb)
        unregisterListener(AddMoleculeCmdEvent, addObjectCmd_cb)
        unregisterListener(EndAddMoleculeEvent, endAddObject_cb)
        unregisterListener(BeforeDeleteMoleculeEvent, beforeDeleteObject_cb)
        unregisterListener(AfterDeleteMoleculeEvent, afterDeleteObject_cb)

        self.assertTrue(self.calls[0]==True)
        self.assertTrue(self.calls[1]==True)
        self.assertTrue(self.calls[2]==True)
        
        app.exit()
        assert sys.getrefcount(app)==2



if __name__ == '__main__':
    import os, testBase
    os.chdir(os.path.split(testBase.__file__)[0])
    unittest.main()
