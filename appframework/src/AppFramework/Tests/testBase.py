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
# Copyright: M. Sanner TSRI 2013
#
#############################################################################

#
# $Header: /mnt/raid/services/cvs/AppFramework/Tests/testBase.py,v 1.1.1.1.4.1 2017/07/28 00:58:01 annao Exp $
#
# $Id: testBase.py,v 1.1.1.1.4.1 2017/07/28 00:58:01 annao Exp $
#
import unittest

class TestBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        from AppFramework.App import AppFramework
        cls.app = app = AppFramework()

    @classmethod
    def tearDownClass(cls):
        cls.app.exit()


if __name__ == '__main__':
    unittest.main()
    
