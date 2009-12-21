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

def initialize():
   ########################################################################
      #Now is time to start populating our configuration file with data
   ########################################################################
   str_value = ""
   conf_values = dict()
   paths = []
   #By default, it attempts to replicate home dir if it is in its own label. 
   if (os.path.isdir('/home')):
      logger.subsection("added home directory '/home' for replication :)")
      paths.append("/home")
      str_value = raw_input("Enter any other directories that may contain user data seperated by commas [e.g /data,/repos]: ")
   else:
      logger.subsection("could not find home partition for synchronization")
      str_value  = raw_input("Enter paths to your user data directories seperated by commas [e.g /data]: ")
   #Do basic error checking to make sure that is a valid directory
   logger.subsection("is "+str_value+" a valid directory[ies]?")
   str_value.replace(' ','')
   if(str_value is not ""):
      paths = paths + str_value.split(',')
   validated_paths = []
   for path in paths:
      if(os.path.isdir(path)):
         logger.subsection(path+" is a valid path")
         validated_paths.append(path)
   count = 0
   path_hash = dict()
   for path in validated_paths:
      path_hash[count] = path
      count += 1
   conf_values['DATA_DIR'] = path_hash

   #For planned future support of other synchronization mechanisms like 
   #DRBD, CSYNC ...
   conf_values['DATA_SYNC'] = "RSYNC"
   #######################################################################
   #We move on to network stuffs
   #This code extracts the list of active interfaces for display to admin
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
   interface_list = [namestr[i:i+32].split('\0',1)[0] for i in range(0, outbytes, 32)]

   if (len(interface_list) == 1):
      logger.subsection("detected only one interface: "+interface_list[0])
      logger.subsection("adding to config file")
      conf_values['NIC_INFO_P'] = interface_list[0]
   else:
      temp = ""
      for i in interface_list:
          temp = temp + i + ", "
      logger.subsection("Detected multiple active interfaces: "+temp)
      str_value = raw_input("Select a network interface from the options above: ")
      str_value = str_value.strip()
      cmd_result = commands.getoutput("ifconfig "+str_value)
      if ('error fetching' in cmd_result or str_value is ""):
         logger.subsection("invalid device specified, skipping for now")
         conf_values['NIC_INFO_P'] = ""
         conf_values['IP_ADDR_P'] = ""
      else:
         logger.subsection("adding interface to config file, proceeding...")
         conf_values['NIC_INFO_P'] =str_value
         logger.subsection("adding ip address of associated interface...")
         ip_addr = socket.inet_ntoa(fcntl.ioctl(
                     s.fileno(),
                     0x8915,
                     struct.pack('256s', str_value[:15])
                     )[20:24])
         conf_values['IP_ADDR_P']=ip_addr

   ########################################################################
   #We finally provide a default list of services to be monitored 'ssh daemon' really

   logger.subsection("generating list of 'default' highly available services")
   conf_values['SERVICES']="sshd"

   #######################################################################
   #Finally, we describe the type of database to be created by our database
   #abstraction method.

   conf_values['DB_TYPE']="sqlite"

   #un-necessary methods, we will use a default uname and password
   #uname = raw_input("Enter database username(only alpha numeric passwords): ")
   #passwd = raw_input("Enter database password(warning input not hashed): ")

   #conf_values['DB_UNAME']=uname
   #conf_values['DB_PASS']=passwd

   #######################################################################

   logger.subsection("finished generating configuration...")
   return conf_values

