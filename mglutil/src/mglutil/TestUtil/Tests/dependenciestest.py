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

#
##########################################################################
#       Author : Sowjanya Karnati
##########################################################################
#
#
#
# Notes:Class that runs the Dependency script and compares with critical and
# noncritical dependencies of the pack 

import os,re
from types import StringType

class DependencyTester:
    
    def rundeptester(self,pack,listdependencies =[],v=True,V=False,loc=None):
        self.pack = pack
        from mglutil.TestUtil import Dependencytester
        deptester = Dependencytester.DEPENDENCYCHECKER()
        Total_packs = deptester.rundependencychecker(pack,v,V,loc)
        if type(self.pack) is not StringType:
            print("pack must be a string")
        result = []
        if listdependencies == []:          
            pat =re.compile('result_%s' %self.pack)
            for a in Total_packs:
                match = pat.search(a)
                if match:
                    listdependencies = eval("a.split('result_%s'%self.pack)[1]")
        ld =eval(listdependencies)
        exec('import %s' %pack)                            
        p=eval(pack)
        try:    
            DEPENDENCIES=p.CRITICAL_DEPENDENCIES+p.NONCRITICAL_DEPENDENCIES                 
            for d in ld:
                if d not in DEPENDENCIES:
                    result.append(d)
            if result!=[]:
                return result
            else:
                return result
        except:
               print("CRITICAL_DEPENDENCIES,NONCRITICAL_DEPENDENCIES not listed in %s.__init__.py" %self.pack)
                            
                            
                    
        
        
        
        
        

    











