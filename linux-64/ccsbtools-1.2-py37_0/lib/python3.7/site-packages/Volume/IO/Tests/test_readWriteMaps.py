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
# Date: Sep 2004  Author: Gabe Lander
#########################################################################
"""Tests the Read/Write functionality and consistency of the Volume
Readers and Writers"""

import types
import numpy
from numbers import Integral as INT
from numbers import Real
import os, sys
import time
from Volume.IO.volReaders import ReadCCP4
from Volume.IO.volWriters import WriteCCP4

timestamp= time.strftime("%Y%m%d%H%M%S")

file1='Data/npma.ccp4'
fileNew='Data/tmp_%s.ccp4'%timestamp

def assertArrayEqual(a1, a2):
    assert len(a1) == len(a2)
    d = abs(a1-a2)
    #print "array shape:", d.shape
    shape = d.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            for k in range(shape[2]):
                assert d[i][j][k] < 1.e-5
                

def test_00_readCCP4file():
    """
    Read a CCP4 file and assert that all the header values
    exist and are of the proper type, and that the dataset is complete
    """

    CCP4reader=ReadCCP4()

    CCP4data=CCP4reader.read(file1,disp_out=False)
    h=CCP4data.header
    d=CCP4data.data
    print("number of keys: ",len(h))
    assert isinstance(h['nc'], INT)
    print("NC: ",h['nc'])
    assert isinstance(h['nr'], INT)
    print("NR: ",h['nr'])
    assert isinstance(h['ns'], INT)
    print("NS: ",h['ns'])
    assert isinstance(h['mode'], INT)
    print("MODE: ",h['mode'])
    assert isinstance(h['ncstart'], INT)
    print("NCSTART: ",h['ncstart'])
    assert isinstance(h['nrstart'], INT)
    print("NRSTART: ",h['nrstart'])
    assert isinstance(h['nsstart'], INT)
    print("NSSTART: ",h['nsstart'])
    assert isinstance(h['nx'], INT)
    print("NX: ",h['nx'])
    assert isinstance(h['ny'], INT)
    print("NY: ",h['ny'])
    assert isinstance(h['nz'], INT)
    print("NZ: ",h['nz'])
    assert isinstance(h['acell'], Real)
    print("X length: ",h['acell'])
    assert isinstance(h['bcell'], Real)
    print("Y length: ",h['bcell'])
    assert isinstance(h['ccell'], Real)
    print("Z length: ",h['ccell'])
    assert isinstance(h['alpha'], Real)
    print("Alpha: ",h['alpha'])
    assert isinstance(h['beta'], Real)
    print("Beta: ",h['beta'])
    assert isinstance(h['gamma'], Real)
    print("Gamma: ",h['gamma'])
    assert isinstance(h['mapc'], INT)
    print("MAPC: ",h['mapc'])
    assert isinstance(h['mapr'], INT)
    print("MAPR: ",h['mapr'])
    assert isinstance(h['maps'], INT)
    print("MAPS: ",h['maps'])
    assert isinstance(h['amin'], Real)
    print("AMIN: ",h['amin'])
    assert isinstance(h['amax'], Real)
    print("AMAX: ",h['amax'])
    assert isinstance(h['amean'], Real)
    print("AMEAN: ",h['amean'])
    assert isinstance(h['ispg'], INT)
    print("ISPG: ",h['ispg'])
    assert isinstance(h['nsymbt'], INT)
    print("NSYMBT: ",h['nsymbt'])
    assert isinstance(h['lskflg'], INT)
    print("LSKFLG: ",h['lskflg'])

    # convert skwmat, skwtrn, and future_words to arrays and check typecode
    assert len(h['skwmat']) is 9    
    assert len(h['skwtrn']) is 3
    assert len(h['future_words']) is 15
    skwmat_array=numpy.array(h['skwmat'])
    skwtrn_array=numpy.array(h['skwtrn'])
    futwrd_array=numpy.array(h['future_words'])
    assert skwtrn_array.dtype.char is 'd'
    assert skwmat_array.dtype.char is 'd'
    assert futwrd_array.dtype.char is 'l'
    print("SKWMAT: ",h['skwmat'])
    print("SKWTRN: ",h['skwtrn'])
    print("future use: ",h['future_words'])

    assert isinstance(h['arms'], Real)
    print("ARMS: ",h['arms'])

    # make sure the data is correct
    dshape=list(d.shape)
    assert sum(dshape)== h['nc']+h['nr']+h['ns']
     
def test_01_readWriteCCP4():
    """
    read a CCP4 map, write it, and compare headers
    to make sure all the header information is the same,
    even if the axes have been reordered.
    Also test that the data sections are the same.
    """

    CCP4reader=ReadCCP4()
    CCP4writer=WriteCCP4()

    CCP4data=CCP4reader.read(file1,disp_out=False)
    CCP4out=CCP4writer.write(fileNew,CCP4data)
    CCP4check=CCP4reader.read(fileNew,disp_out=False)

    h_orig=CCP4data.header
    h_new=CCP4check.header
    d_orig=CCP4data.data
    d_new=CCP4check.data
    
    orig_vals = list(h_orig.values())
    new_vals = list(h_new.values())

    #sum up values of all ints and floats separately, and compare
    orig_intSum = sum([x for x in orig_vals if isinstance(x, INT)])
    new_intSum = sum([x for x in new_vals if isinstance(x, INT)])
    orig_flSum = sum([x for x in orig_vals if isinstance(x, Real)])
    new_flSum = sum([x for x in new_vals if isinstance(x, Real)])

    #floats aren't always exact, but close enough.  Round to 3 decimals.
    orig_flSum = "%.3f" %orig_flSum
    new_flSum = "%.3f" %new_flSum

    assert orig_intSum == new_intSum
    assert orig_flSum == new_flSum
    assertArrayEqual(d_orig, d_new)
    
    #remove newly created test file
    os.remove(fileNew)

def test_02_checkCCP4syminfo():
    """
    If symmetry information exists in the file,
    make sure that it appears in the output file
    """

    CCP4reader=ReadCCP4()
    CCP4writer=WriteCCP4()
    
    CCP4data=CCP4reader.read(file1,disp_out=False)
    CCP4out=CCP4writer.write(fileNew,CCP4data)
    CCP4check=CCP4reader.read(fileNew,disp_out=False)

    h_orig=CCP4data.header
    h_new=CCP4check.header

    len_orig = os.stat(file1)[6]
    len_new = os.stat(fileNew)[6]

    len_orig_data=h_orig['nc']*h_orig['nr']*h_orig['ns']*4
    len_new_data=h_new['nc']*h_new['nr']*h_new['ns']*4
    len_orig_sym=h_orig['nsymbt']
    len_new_sym=h_new['nsymbt']
    len_orig_exp = len_orig_data + len_orig_sym + 1024
    len_new_exp = len_new_data + len_new_sym + 1024

    # if the length of the original file is less than the expected length,
    # then it must be missing the symmetry info.
    if len_orig < len_orig_exp:
        print(file1, " is missing symmetry info")
        assert len_orig + len_orig_sym == len_orig_exp
    else:
        assert len_orig == len_orig_exp

    # the output file should always have a space for symmetry info
    assert len_new == len_new_exp

    #remove newly created test file
    os.remove(fileNew)
