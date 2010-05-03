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
from marshal import dumps
import halib.Logger as logger
import halib.chaif.DatabaseDriver as ddriver

#@des:The systemConfigurator retrieves critical system facts
#     It gets information about network interface, hdd partitioning and other
#     things needed.
class SysConfigurator:
    
    def __init__(self):
        self.str_value = ""
        self.conf_values = dict()
        self.paths = []
        self.validated_paths = ""
        self.interface_list = []
        self.ip_addr = ""
   
    #Appropriate method to call when trying to gather configuration data 
    def priConfig(self):
        self.dataConfig()
        self.netConfig()
        self.serviceConfig()
        self.hostnameConfig()
        logger.subsection("finished generating configuration...")
        return self.conf_values

    #Should be called after configuring primary config server
    def secConfig(self):
      sec_config = dict()
      temp = ""
      temp = raw_input("enter the host name of the secondary server: ")
      if (temp is not None):#Perform some basic error check.
                            #TODO: Ensure only alphanumeric characters
         sec_config['HOSTNAME'] = temp
      database_driver = ddriver.DbDriver()
      config =  database_driver.select_db("Primary_Configuration")
      sec_config['NIC_INFO'] = config[0]['NIC_INFO'] 
      sec_config['IP_ADDR'] = raw_input("enter a valid ip addr for secondary server: ")
      return sec_config
    
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
          self.str_value  = raw_input("Enter paths to your user data directories seperated by commas [e.g /data,/repos]: ")
       #Do basic error checking to make sure that is a valid directory
       logger.subsection("is "+self.str_value+" a valid directory[ies]?")
       #self.str_value = self.str_value.replace(" ","")  #this means paths with spaces eg: /my\ path/ are not supported. Should be split up, then leading and trailing whitespace truncated. 
       if(self.str_value is not '' and not self.str_value.isspace()): #rejects any "empty" path list
          self.paths = self.paths + self.str_value.split(',')
       for path in self.paths:
          path = path.strip() #strips whitespace from front and back, leaving middle spaces intact.
          if(os.path.exists(path)):
             logger.subsection(path+" is a valid path")
             self.validated_paths += path+";"
      
       self.conf_values['DATA_DIR'] = self.validated_paths
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
       self.interface_list = [namestr[i:i+32].split('\0',1)[0] for i in
range(0, outbytes, 32)] #TODO: Fix parsing
       if (len(self.interface_list) == 1):  #shouldn't ever happen, and would break as written.
          logger.subsection("detected only one interface: "+self.interface_list[0])
          logger.subsection("adding to config file")
          self.conf_values['NIC_INFO'] = self.interface_list[0]
       else:
          temp = ""
          for i in self.interface_list:
              temp = temp + i + ", "
          temp = temp.strip(', ') #cleans off tailing comma
          logger.subsection("Detected multiple active interfaces: "+temp)
          self.str_value = raw_input("Select the local network interface from the options above. If you would like to only migrate specific interfaces on failure, list them after the local interface seperated by commas: ")
          ha_ifaces = self.str_value.partition(',') #[0] contains local interface. [3] contains rest.
          self.str_value = ha_ifaces[0].strip()
          cmd_result = commands.getoutput("ifconfig "+self.str_value)
          if ('error fetching' in cmd_result or self.str_value is ""):
             logger.subsection("invalid device specified, skipping for now")
             self.conf_values['NIC_INFO'] = ""
             self.conf_values['IP_ADDR'] = ""
          else:
             logger.subsection("adding interface to config file, proceeding...")
             self.conf_values['NIC_INFO'] =self.str_value
             logger.subsection("adding ip address of associated interface...")
             self.ip_addr = socket.inet_ntoa(fcntl.ioctl(
                         s.fileno(),
                         0x8915,
                         struct.pack('256s', self.str_value[:15])
                         )[20:24])
             self.conf_values['IP_ADDR']=self.ip_addr
             
             logger.subsection("setting up netmask and subnet...")
             maskline = commands.getoutput("echo \""+cmd_result+"\" | grep Mask:")
             self.conf_values['MASK'] = maskline.partition('Mask:')[2] #retrieves the proper netmask
             masksub = self.conf_values['MASK'].partition('.')
             ipsub = self.conf_values['IP_ADDR'].partition('.')
             self.conf_values['SUBNET'] = ''
             for i in range(2):
               self.conf_values['SUBNET'] += str(int(masksub[0]) & int(ipsub[0])) + '.'  #Gets next section
               masksub = masksub[2].partition('.')
               ipsub = ipsub[2].partition('.')
             self.conf_values['SUBNET'] += str(int(masksub[0]) & int(ipsub[0])) + '.' #2nd to last
             self.conf_values['SUBNET'] += str(int(masksub[2]) & int(ipsub[2]))  #Gets the last section
          
          self.conf_values['FALLBACK_IPS'] = ''
          if ha_ifaces[1] == ',': #We have specified interfaces.
            while ha_ifaces[1] == ',':
              ha_ifaces = ha_ifaces[0].partition(',')
              ha_ifaces[0] = socket.inet_ntoa(fcntl.ioctl(
                         s.fileno(),
                         0x8915,
                         struct.pack('256s', ha_ifaces[0].strip()[:15])
                         )[20:24])
              self.conf_values['FALLBACK_IPS'] += ' ' + ha_ifaces[0]  #Leading space should be left intact.
          else: #We should use all availavle interfaces except lo.
            for interface in self.interface_list:
              if interface != 'lo' and interface != self.conf_values['NIC_INFO']:
                ha_ip = socket.inet_ntoa(fcntl.ioctl(
                         s.fileno(),
                         0x8915,
                         struct.pack('256s', interface[:15])
                         )[20:24])
                self.conf_values['FALLBACK_IPS'] += ' ' + ha_ip
          self.conf_values['FALLBACK_IPS'] = self.conf_values['FALLBACK_IPS'].strip()
          
    ########################################################################
    #We finally provide a default list of services to be monitored 'ssh daemon' really
    #and the HA-DAEMON
       
    def serviceConfig(self):
       logger.subsection("generating list of 'default' highly available services")
       self.conf_values['SERVICES']="sshd"
    
    #######################################################################
    #Finally, we describe the type of database to be created by our database
    #abstraction method.
    #def databaseConfig(self):
       #self.conf_values['DB_TYPE']="sqlite"
    
       #un-necessary methods, we will use a default uname and password
       #uname = raw_input("Enter database username(only alpha numeric passwords): ")
       #passwd = raw_input("Enter database password(warning input not hashed): ")
    
       #conf_values['DB_UNAME']=uname
       #conf_values['DB_PASS']=passwd
    
       #######################################################################
    def hostnameConfig(self):
      self.conf_values['HOSTNAME'] =commands.getoutput("uname -n")
       

