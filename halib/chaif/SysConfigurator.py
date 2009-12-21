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

import os
import socket
import fcntl
import struct
import array
import commands
import halib.Logger as logger

#@des:The systemConfigurator retrieves critical system facts
#     It gets information about network interface, hdd partitioning and other
#     things needed.
class SysConfigurator:
    
    def __init__(self):
        self.str_value = ""
        self.conf_values = dict()
        self.paths = []
        self.validated_paths = []
        self.interface_list = []
        self.ip_addr = ""
   
    #Appropriate method to call when trying to gather configuration data 
    def initialize(self):
        self.dataConfig()
        self.netConfig()
        self.serviceConfig()
        self.databaseConfig()
        logger.subsection("finished generating configuration...")
        return conf_values
    
    def dataConfig(self):
       ########################################################################
          #Now is time to start populating our configuration file with data
       ########################################################################
       #By default, it attempts to replicate home dir if it is in its own label. 
       if (os.path.isdir('/home')):
          logger.subsection("added home directory '/home' for replication :)")
          self.paths.append("/home")
          self.str_value = raw_input("Enter any other directories that may contain user data seperated by commas [e.g /data,/repos]: ")
       else:
          logger.subsection("could not find home partition for synchronization")
          self.str_value  = raw_input("Enter paths to your user data directories seperated by commas [e.g /data]: ")
       #Do basic error checking to make sure that is a valid directory
       logger.subsection("is "+self.str_value+" a valid directory[ies]?")
       self.str_value = self.str_value.replace(" ","")
       if(self.str_value is not ""):
          self.paths = self.paths + self.str_value.split(',')
       for path in self.paths:
          if(os.path.exists(path)):
             logger.subsection(path+" is a valid path")
             self.validated_paths.append(path) #TODO: Fix truncation bug that exists and no duplicates
    
       count = 0
       path_hash = dict()
       #print "DEBUG: Original Paths are: ",paths
       #print "DEBUG: Validated Paths are: ",validated_paths
       for path in self.validated_paths:
          path_hash[count] = path
          count += 1
       self.conf_values['DATA_DIR'] = path_hash
    
       #For planned future support of other synchronization mechanisms like 
       #DRBD, CSYNC ...
       self.conf_values['DATA_SYNC'] = "RSYNC"   
    #######################################################################
    #We move on to network stuffs
    #This code extracts the list of active interfaces for display to admin
    ######################################################################
    def netConfig(self):
       max_possible = 128 #Max no of interfaces
       bytes = max_possible * 32
       s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       names = array.array('B', '\0' * bytes)
       outbytes = struct.unpack('iL', fcntl.ioctl(
                               s.fileno(),
                               0x8912, #SIOCGIFCONF
                               struct.pack('iL',bytes, names.buffer_info()[0]
                               )))[0]
       namestr = names.tostring()
       self.interface_list = [namestr[i:i+32].split('\0',1)[0] for i in range(0, outbytes, 32)]
    
       if (len(self.interface_list) == 1):
          logger.subsection("detected only one interface: "+self.interface_list[0])
          logger.subsection("adding to config file")
          self.conf_values['NIC_INFO_P'] = self.interface_list[0]
       else:
          temp = ""
          for i in self.interface_list:
              temp = temp + i + ", "
          logger.subsection("Detected multiple active interfaces: "+temp)
          self.str_value = raw_input("Select a network interface from the options above: ")
          self.str_value = str_value.strip()
          cmd_result = commands.getoutput("ifconfig "+self.str_value)
          if ('error fetching' in cmd_result or self.str_value is ""):
             logger.subsection("invalid device specified, skipping for now")
             self.conf_values['NIC_INFO_P'] = ""
             self.conf_values['IP_ADDR_P'] = ""
          else:
             logger.subsection("adding interface to config file, proceeding...")
             self.conf_values['NIC_INFO_P'] =self.str_value
             logger.subsection("adding ip address of associated interface...")
             self.ip_addr = socket.inet_ntoa(fcntl.ioctl(
                         s.fileno(),
                         0x8915,
                         struct.pack('256s', self.str_value[:15])
                         )[20:24])
             self.conf_values['IP_ADDR_P']=self.ip_addr
    
    ########################################################################
    #We finally provide a default list of services to be monitored 'ssh daemon' really
    #and the HA-DAEMON
       
    def serviceConfig(self):
       logger.subsection("generating list of 'default' highly available services")
       self.conf_values['SERVICES']="sshd"
    
    #######################################################################
    #Finally, we describe the type of database to be created by our database
    #abstraction method.
    def databaseConfig(self):
       conf_values['DB_TYPE']="sqlite"
    
       #un-necessary methods, we will use a default uname and password
       #uname = raw_input("Enter database username(only alpha numeric passwords): ")
       #passwd = raw_input("Enter database password(warning input not hashed): ")
    
       #conf_values['DB_UNAME']=uname
       #conf_values['DB_PASS']=passwd
    
       #######################################################################
    
       

