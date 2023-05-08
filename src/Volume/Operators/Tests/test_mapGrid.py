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

import numpy

arrInt = numpy.ones( (5,5,5), 'i')
arrFloat = numpy.ones( (5,5,5), 'i')
arrValues = numpy.arange(125)
arrValues.shape = (5,5,5)

from Volume.Operators.MapData import MapGridData
mapper = MapGridData()

def test_mapIntToFloat():
    result = mapper(arrInt, datatype=numpy.float32)
    assert result.dtype.char==numpy.float32
    assert result.shape==(5,5,5)

def test_mapFloatToInt():
    result = mapper(arrFloat, datatype=numpy.int32)
    assert result.dtype.char==numpy.int32
    assert result.shape==(5,5,5)
    
def test_mapPowerOf2():
    result = mapper(arrValues, powerOf2=True)
    #assert result.dtype.char==arrFloat.dtype.char
    assert result.shape==(8,8,8)

def test_fromlist():
    arrlist = arrFloat.tolist()
    result = mapper(arrInt, datatype=numpy.float32)
    assert result.dtype.char==numpy.float32
    assert result.shape==(5,5,5)
    
def test_mapping1():
    datamap = {}
    datamap['src_min'] = None
    datamap['src_max'] = None
    datamap['dst_min'] = 0
    datamap['dst_max'] = 248
    datamap['map_type'] = 'linear'
    result = mapper(arrValues, datamap=datamap)
    assert result.dtype.char==arrValues.dtype.char
    assert numpy.maximum.reduce(result.ravel())==248
    assert numpy.minimum.reduce(result.ravel())==0

def test_mapping2():
    datamap = {}
    datamap['src_min'] = 50
    datamap['src_max'] = 100
    datamap['dst_min'] = 0
    datamap['dst_max'] = 248
    datamap['map_type'] = 'linear'
    result = mapper(arrValues, datamap=datamap)
    assert result.dtype.char==arrValues.dtype.char
    assert numpy.maximum.reduce(result.ravel())==248
    assert numpy.minimum.reduce(result.ravel())==0
    assert result[2,0,0] == 0 and arrValues[2,0,0]==50
    assert numpy.minimum.reduce(result[:2,0,0]) == 0
    assert numpy.maximum.reduce(result[:2,0,0]) == 0
    assert numpy.maximum.reduce(result[4:,0,0]) == 248
    assert numpy.minimum.reduce(result[4:,0,0]) == 248


def test_mapAndConvert():
    datamap = {}
    datamap['src_min'] = 50
    datamap['src_max'] = 100
    datamap['dst_min'] = 0
    datamap['dst_max'] = 248
    datamap['map_type'] = 'linear'
    result = mapper(arrValues, datamap=datamap, datatype=numpy.float32)
    assert result.dtype.char==numpy.float32
    assert numpy.maximum.reduce(result.ravel())==248.
    assert numpy.minimum.reduce(result.ravel())==0.
    assert result[2,0,0] == 0 and arrValues[2,0,0] == 50.
    assert numpy.minimum.reduce(result[:2,0,0]) == 0.
    assert numpy.maximum.reduce(result[:2,0,0]) == 0.
    assert numpy.maximum.reduce(result[4:,0,0]) == 248.
    assert numpy.minimum.reduce(result[4:,0,0]) == 248.

