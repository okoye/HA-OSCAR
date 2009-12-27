#! /usr/bin/env python
#
# Copyright (c) 2009 Okoye Chuka D.<okoye9@gmail.com>
#                    All rights reserved.
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
 
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
 
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

#Unit tests for the Gathering Framework

import sys
sys.path.append("../")
import halib.haframework.Gather as gather
import unittest
import commands

class TestGatherFunctions(unittest.TestCase):
   def setUp(self):
      #string = "cp /home/okoye/test_module_1.py /usr/share/haoscar/Gather/"
      #commands.getoutput(string)
      pass


   #Test the reset function
   def test_reset(self):
      x = gather.reset()
      self.failIf(x is False)

   def tearDown(self):
      #commands.getouput("rm /usr/share/haoscar/Gather/test_module_0.py")
      #commands.getoutput("rm /usr/share/hoscar/Gather/test_module_1.py")
      pass


if __name__ == '__main__':
   unittest.main()
