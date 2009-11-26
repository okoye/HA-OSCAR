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
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  US

from os import system 
from os import path
import commands
import socket
import fcntl
import struct
import array
import halib.Logger as logger
import halib.chaif.DatabaseDriver as ddriver
import halib.chaif.SanityCheck as scheck
import halib.chaif.RemoteServices as remote
import halib.Exit as exit


#@des:	The sanityCheck method ensure the build environment is sane
#			It checks, operating sys, user as root, sshd root login.		

def sanityCheck():
	logger.subsection("checking to make sure system environment is sane")
	err = scheck.initialize()
	if(len(err) > 0):
		logger.subsection("the following errors resulted from sanity check:")
		for message in err:
			logger.subsection(message)
		logger.subsection("installation cannot continue")
		return 1
	else:
		logger.subsection("yup, system is sane")
		return 0

def databaseSetup():
	logger.subsection("starting mysql services")
	system("/etc/init.d/mysqld restart")
	logger.subsection("initializing database")
	#Create database
	ddriver.create_db()
	logger.subsection("database setup completed sucessfully")

def remoteSetup():
	logger.subsection("initializing remote services library")
	remote.initialize()
	logger.subsection("remote services initalization completed")

#@des:	The systemConfigurator method retrieves critical system facts
#		It gets information about network interface, hdd partitioning and other
#		things needed.

def systemConfigurator():
	########################################################################
		#Now is time to start populating our configuration file with data
	########################################################################
	str_value = ""
	conf_values = dict()
	#this currently works only on systems with the by-label defined(most redhatbased)
	cmd_output = commands.getoutput("ls /dev/disk/by-label")
	if ("home" in cmd_output):
		logger.subsection("the file system home has a label :)")
		conf_values['DATA_DIR'] = commands.getoutput("findfs LABEL/home")
	else:
		logger.subsection("could not find home partition label")
		str_value  = raw_input("Enter the device identificaton of your data partition example /dev/sda0 for scsi disks or /dev/hd[e|a]0 for ide: ")
		#Do basic error checking to make sure that is a valid device
		logger.subsection("is "+str_value+" a valid device?")
		str_value = str_value.strip()
		cmd_result = commands.getoutput("e2label "+str_value)
		if('superblock' in cmd_result or str_value is ""): #Improper method to check for bad device blocks
			logger.subsection("nope, invalid device, skipping for now")
			conf_values['DATA_DIR'] = ""
		else:
			logger.subsection("yep, congratulations we can proceed...")
			conf_values['DATA_DIR'] = str_value
	
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
		conf_values['NIC_INFO'] = interface_list[0]
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
			conf_values['NIC_INFO'] = ""
			conf_values['IP_ADDR'] = ""
		else:
			logger.subsection("adding interface to config file, proceeding...")
			conf_values['NIC_INFO'] =str_value
			logger.subsection("adding ip address of associated interface...")
			ip_addr = socket.inet_ntoa(fcntl.ioctl(
							s.fileno(),
							0x8915,
							struct.pack('256s', str_value[:15])
							)[20:24])
			conf_values['IP_ADDR']=ip_addr
	
	########################################################################
	#We finally provide a default list of services to be monitored 'ssh daemon' really
	
	logger.subsection("generating list of 'default' highly available services")
	conf_values['SERVICES']="sshd"
	
	#######################################################################
	#Finally, we describe the type of database to be created by our database
	#abstraction method.
	
	conf_values['HA_DB_TYPE']="mysql"
	
	#un-necessary methods, we will use a default uname and password
	#uname = raw_input("Enter database username(only alpha numeric passwords): ")
	#passwd = raw_input("Enter database password(warning input not hashed): ")
	
	#conf_values['DB_UNAME']=uname
	#conf_values['DB_PASS']=passwd
	
	#######################################################################
	
	logger.subsection("finished generating configuration...")
	return conf_values
