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
# Author: Michel F. SANNER
#
# Copyright: M. Sanner TSRI 2014
#
#############################################################################

#
# $Header: /mnt/raid/services/cvs/PmvApp/GUI/Qt/Tests/testBase.py,v 1.3.4.1 2017/07/13 20:47:44 annao Exp $
#
# $Id: testBase.py,v 1.3.4.1 2017/07/13 20:47:44 annao Exp $
#
import unittest, sys

class TestBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        from PySide import QtGui, QtCore
        try:
            cls.app = app = QtGui.QApplication(sys.argv)
        except RuntimeError:
            pass
        from PmvApp.Pmv import MolApp
        cls.pmv = pmv = MolApp()
        pmv.trapExceptions = False
        pmv.lazyLoad('bondsCmds', package='PmvApp')
        pmv.lazyLoad('fileCmds', package='PmvApp')
        pmv.lazyLoad('displayCmds', package='PmvApp')
        pmv.lazyLoad("colorCmds", package='PmvApp')
        pmv.lazyLoad("selectionCmds", package='PmvApp')
        pmv.lazyLoad("deleteCmds", package='PmvApp')
        pmv.lazyLoad('msmsCmds', package='PmvApp')
        
        from PmvApp.GUI.Qt.PmvGUI import PmvGUI
        cls.gui = PmvGUI(pmv)
        cls.gui.resize(800,600)
        #sys.exit(app.exec_())

    @classmethod
    def tearDownClass(cls):
        cls.pmv.exit()
        #cls.app.exit()

if __name__ == '__main__':
    unittest.main()
