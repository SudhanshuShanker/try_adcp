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
from time import sleep
from mglutil.gui.BasicWidgets.Tk.xyzGUI import xyzGUI
widget = None
wasCalled = 0

def pause(sleepTime=0.2):
    widget.master.update()
    sleep(sleepTime)

class  XYZGUIBaseTest(unittest.TestCase):
    def test_constructor(self):
        # test if we can display the xyzGUI (consists of 3 thumbwheels)
        global widget
        widget = xyzGUI()
        pause(0.6)
        widget.master.destroy()

if __name__ == '__main__':
    unittest.main()
