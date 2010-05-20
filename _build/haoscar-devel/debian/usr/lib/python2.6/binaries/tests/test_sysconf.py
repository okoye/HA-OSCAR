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
import commands
import os
import unittest

class TestConfigFunctions(unittest.TestCase):
  def setUp(self):
    self.sconf = sysconfig.SysConfigurator()
    self.iflines = []
    self.ifstring = ""
    self.interface_list = [] #Local parsing of adapter list based on ifconfig.
  
  def test_dataconfig(self):
    sys.stdin = file('input/dcfg') #Used to automate input.
    
    #check for /cont space/full path/. If it doesn't exist, make it, and flag that I made it.
    madeit = 0
    if (os.path.isdir('/cont space')):
      if not(os.path.isdir('/cont space/full path')):
        os.mkdir('/cont space/full path')
        madeit = 1
    else:
      os.mkdir('/cont space')
      os.mkdir('/cont space/full path')
      madeit = 2
    
    #run tests
    try:
      self.sconf.dataConfig()
      self.assertEquals(self.sconf.validated_paths, "/home;")
      self.sconf.paths = [] #clear path and validated_paths to prevent conflict.
      self.sconf.validated_paths = ""
      self.sconf.dataConfig()
      self.assertEquals(self.sconf.validated_paths, "/home;/etc;/cont space/full path;")
    except: #included to cleanup even on fail.
      if madeit >= 1:
        os.rmdir('/cont space/full path')
      if madeit == 2:
        os.rmdir('/cont space')
      raise
    #if I made /cont space/full path/, delete it.
    if madeit >= 1:
      os.rmdir('/cont space/full path')
    if madeit == 2:
      os.rmdir('/cont space')

  def test_netconfig(self):
    sys.stdin = file('input/ncfg') #Used to automate input.
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
    self.assertEquals(numadapter, 0)  #Each adapter from ifconfig exists exactly once.
    self.assertEquals(self.sconf.conf_values['NIC_INFO'], 'lo') #The scrips selected 'lo'
    self.assertEquals(self.sconf.ip_addr,'127.0.0.1') #lo is 127.0.0.1
    self.assertEquals(self.sconf.conf_values['MASK'],'255.0.0.0')
    self.assertEquals(self.sconf.conf_values['SUBNET'],'127.0.0.0')

  def test_serviceconfig(self):
    self.sconf.serviceConfig()
    self.assertEquals(self.sconf.conf_values['SERVICES'], 'sshd')

  def test_hostnameconfig(self):
    self.sconf.hostnameConfig()
    self.assertEquals(self.sconf.conf_values['HOSTNAME'], commands.getoutput("uname -n"))

#sys.stdin = sys.__stdin__ #resumes manual input

if __name__ == '__main__':
  unittest.main()
