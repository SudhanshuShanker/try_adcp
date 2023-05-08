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
# Date: Jun 2002 Authors: Daniel Stoffler, Michel Sanner
#
#    stoffler@scripps.edu
#    sanner@scripps.edu
#
# Copyright:  Daniel Stoffler, Michel Sanner, and TSRI
#
#########################################################################

import sys,unittest
from mglutil.regression import testplus
from time import sleep
from mglutil.gui.BasicWidgets.Tk.vector3DGUI import vectorGUI
widget = None
wasCalled = 0

def pause(sleepTime=0.2):
    widget.master.update()
    sleep(sleepTime)


class Vector3DGUIBaseTest(unittest.TestCase):

    def test_constructor(self):
        # test if we can display a vectorGUI
        global widget
        widget = vectorGUI(size=100)
        pause()
        widget.master.destroy()

    
    def test_setPrecision(self):
        global widget
        from mglutil.gui.BasicWidgets.Tk.vector3DGUI import vectorGUI
        widget = vectorGUI(size=100)
        widget.configure(type='float')
        widget.configure(precision=5)
        # increase precision to 5 - this is only visual. value is not changed
        self.assertEqual(widget.precision == 5,True)
        pause()
        widget.master.destroy()


    def test_setContinuous(self):
        global widget
        from mglutil.gui.BasicWidgets.Tk.vector3DGUI import vectorGUI
        widget = vectorGUI(size=100)
        widget.configure(continuous=1)
        self.assertEqual(widget.continuous == 1,True)
        widget.configure(continuous=0)
        self.assertEqual(widget.continuous == (0 or None),True)
        pause()
        widget.master.destroy()


    def test_setMode(self):
        global widget
        from mglutil.gui.BasicWidgets.Tk.vector3DGUI import vectorGUI
        widget = vectorGUI(size=100)
        widget.configure(mode='XY')
        self.assertEqual(widget.mode == 'XY',True)
        widget.configure(mode='X')
        self.assertEqual(widget.mode == 'X',True)
        widget.configure(mode='Y')
        self.assertEqual(widget.mode == 'Y',True)
        widget.configure(mode='Z')
        self.assertEqual(widget.mode == 'Z',True)
        pause()
        widget.master.destroy()


    def test_setVector(self):
        # setVector does NOT call callback
        global widget
    
        def foo(val):
            global wasCalled
            print("I should not be called")
            wasCalled=1
    
        from mglutil.gui.BasicWidgets.Tk.vector3DGUI import vectorGUI
        widget = vectorGUI(size=100)
        widget.setVector([1.0,0.0,0.0])
        if wasCalled:
            raise RuntimeError
        widget.master.destroy()

    

if __name__ == '__main__':
   unittest.main() 
