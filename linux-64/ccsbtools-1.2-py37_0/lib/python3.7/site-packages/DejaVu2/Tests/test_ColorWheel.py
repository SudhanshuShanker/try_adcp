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

## Automatically adapted for numpy.oldnumeric Jul 23, 2007 by 

#
#
# $Id: test_ColorWheel.py,v 1.1.1.1.4.1 2017/07/13 22:24:00 annao Exp $
#
#
import tkinter
import numpy
import numpy.oldnumeric as Numeric, math
import DejaVu2.colorTool
import DejaVu2.Slider
from DejaVu2.EventHandler import CallbackFunctions
import unittest
from DejaVu2.ColorWheel import ColorWheel
from DejaVu2.colorTool import ToRGB,ToHSV
def MyCallback(color):
	print(color)
def MyCallback2(color):
	print('hello')


class ColorWheel_BaseTests(unittest.TestCase):

    def test_colorwheel_visible(self):
        """check that one colorwheel is visible after building 3
        """
        root = tkinter.Tk()
        cw = ColorWheel(root)
        cw.AddCallback(MyCallback)
        cw1 = ColorWheel(root, immediate=0)
        cw1.AddCallback(MyCallback2)
        cw2 = ColorWheel(root, immediate=0)
        cw1.AddCallback(MyCallback)
        cw2.AddCallback(MyCallback2)
        root.wait_visibility(cw.canvas)
        root.wait_visibility(cw1.canvas)
        root.wait_visibility(cw2.canvas)
        self.assertEqual(cw.canvas.master.winfo_ismapped(),True)
        self.assertEqual(root.winfo_ismapped(),True)
        root.destroy()

    def test_colorwheel_add_remove_callback(self):
        root = tkinter.Tk()
        cw = ColorWheel(root)
        cw.AddCallback(MyCallback)
        root.wait_visibility(cw.canvas)
        self.assertEqual(len(cw.callbacks),1)
        cw.RemoveCallback(MyCallback)
        self.assertEqual(len(cw.callbacks),0)
        root.destroy()

    def test_colorwheel_height(self):
        """check height of colorwheel
        """
        root = tkinter.Tk()
        cw = ColorWheel(root)
        cw.height = 120
        cw.AddCallback(MyCallback)
        root.wait_visibility(cw.canvas)
        #apparently there is a 10 pixel border on each edge:
        self.assertEqual(cw.canvas.cget('height'), str(100))
        root.destroy()
        
    def test_colorwheel_cursor(self):
        """tests color wheel,moving cursor
        """
        root = tkinter.Tk()
        cw = ColorWheel(root)
        old_x = cw.cursorX        
        old_y = cw.cursorY
        cw._MoveCursor(25,25)
        new_x = cw.cursorX
        new_y = cw.cursorY
        root.wait_visibility(cw.canvas)
        self.assertEqual(old_x != new_x,True)
        self.assertEqual(old_y != new_y,True)
        root.destroy()

    
    def test_colorwheel_color_1(self):
        """test colorwheel,colors after moving cursor
        """
        root = tkinter.Tk()
        cw = ColorWheel(root)    
        old_color = cw.hsvColor
        cw._MoveCursor(25,25)
        new_color = cw.hsvColor
        root.wait_visibility(cw.canvas)
        #self.assertEqual(old_color,new_color)
        self.assertTrue(numpy.alltrue(old_color==new_color))
        cw.Set((1.0,0.0,0.0),mode = 'RGB')
        mycolor = ToRGB(cw.Get())
        mycol =[]
        for i in range(0,4):
            mycol.append(round(mycolor[i]))
        self.assertEqual(mycol,[1.0,0.0,0.0,1.0])
        root.destroy()

    def test_colorwheel_color_HSV(self):
        """test colorwheel,when mode is hsv
        """
        root = tkinter.Tk()
        cw = ColorWheel(root)
        cw.Set((1.0,0.0,0.0),mode = 'HSV')
        root.wait_visibility(cw.canvas)
        self.assertEqual(cw.hsvColor,[1.0, 0.0, 0.0, 1.0])
        self.assertEqual(cw.cursorX,50)
        self.assertEqual(cw.cursorY,50)
        root.destroy()


    def test_colorwheel_color_RGB(self):
        """test colorwheel,when mode is rgb
        """
        root = tkinter.Tk()
        cw = ColorWheel(root)
        cw.Set((1.0,0.0,0.0),mode = 'RGB')
        root.wait_visibility(cw.canvas)
        self.assertEqual(cw.cursorX,100)
        self.assertEqual(cw.cursorY,50)
        self.assertEqual(cw.hsvColor[:3] != [1.0, 0.0, 0.0],True)
        root.destroy()
        
    def test_colorwheel_Wysiwyg(self):
        """test colorwheel,when Wysiwyg On
        """
        root = tkinter.Tk()
        cw = ColorWheel(root)
        cw.Set((1.0,0.0,0.0),mode = 'HSV')    
        #when on wheel colors are recomputed
        cw.setWysiwyg(1)
        root.wait_visibility(cw.canvas)
        self.assertEqual(cw.hsvColor == [1.0, 0.0, 0.0, 1.0],True)
        cw.setWysiwyg(0)
        #root.wait_visibility(cw.canvas)
        self.assertEqual(cw.hsvColor[:3] != [1.0, 0.0, 0.0],True)
        root.destroy()

    def test_colorwheel_keyword_arguements(self):
        """tests setting keyword arguements in colorwheel
        """
        root = tkinter.Tk()
        cw = ColorWheel(root,circles = 20,stripes = 20,width =160,height =160)          
        self.assertEqual(cw.circles,20)
        self.assertEqual(cw.width,160)
        self.assertEqual(cw.height,160)
        self.assertEqual(cw.stripes,20)
        root.destroy()

    
        


if __name__ == '__main__':
    unittest.main()
