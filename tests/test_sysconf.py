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

#   Unit tests for SysConfigurator in CHAIF

import sys
sys.path.append("../")
import halib.chaif.SysConfigurator as sysconfig
import unittest
import commands

class TestConfigFunctions(unittest.TestCase):
  def setUp(self):
    self.sconf = sysconfig.SysConfigurator()
    self.iflines = []
    self.ifstring = ""
    self.interface_list = [] #Local parsing of adapter list based on ifconfig.
    sys.stdin = file('cfginput') #Used to automate input.
  
  def test_dataconfig(self):
    self.sconf.dataConfig()
    self.assertEquals(self.sconf.validated_paths, "/home;")
    self.sconf.paths = [] #clear path and validated_paths to prevent conflict.
    self.sconf.validated_paths = ""
    self.sconf.dataConfig()
    self.assertEquals(self.sconf.validated_paths, "/home;/etc;/cont space/full path;")

  def test_netconfig(self):
    sys.stdin = sys.__stdin__ #resumes manual input
    self.sconf.netConfig()
    iflines = commands.getoutput("ifconfig | grep [[:alnum:]]\ \ \ ").splitlines() #returns only the lines that contain adapter names.
    numadapter = 0    #tracks how many adapters we found to ID if they're all there in the sysconfig
    for line in iflines:
      self.ifstring = line.partition(' ')[0] #grabs the part before the spaces and stores it as a string
      self.interface_list.append(self.ifstring) #stores the string as a single element
      numadapter += 1
    for interface in self.sconf.interface_list:
      if interface in self.interface_list:
        numadapter -= 1
    self.assertEquals(numadapter, 0)

if __name__ == '__main__':
  unittest.main()