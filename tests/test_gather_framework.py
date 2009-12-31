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
import halib.chaif.DatabaseDriver as ddriver
import unittest
import commands

class TestGatherFunctions(unittest.TestCase):
   def setUp(self):
      commands.getoutput("mkdir -p /usr/share/haoscar/Gather")
      string = "cp /home/okoye/test_module_1.py /usr/share/haoscar/Gather/"
      commands.getoutput(string)
      commands.getoutput("touch /usr/share/haoscar/Gather/test_module_0.py")
      
   def test_reset(self):
      x = gather.reset()
      self.failIf(x is False)

   def test_getActiveModules(self):
      x = None
      x = gather.getActiveModules()
      self.failIf("test_module_0.py" in x)
      self.assert_(x != None )

   def test_getAllModules(self):
      x = None
      x = gather.getAllModules()
      self.failIf(x == None)

   def test_removeActiveModules(self):
      database_driver = ddriver.DbDriver()
      active_modules = []

      x = gather.removeActiveModules(["Ganglia_Monitor_Test"])

      active_modules = database_driver.select_db("Active_Modules")

      for index in xrange(len(active_modules)):
         self.failIf(active_modules[index]["NAME"] is "Ganglia_Monitor_Test")
      self.assert_(x == True)
            

   def tearDown(self):
      commands.getoutput("rm /usr/share/haoscar/Gather/test_module_0.py")
      commands.getoutput("rm /usr/share/hoscar/Gather/test_module_1.py")
      pass

if __name__ == '__main__':
   unittest.main()
