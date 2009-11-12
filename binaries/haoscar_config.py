#! /usr/bin/env python
#
# Copyright (c) 2009 Okoye Chuka D. <okoye9@gmail.com>         
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

import sys
sys.path.append("../")
from os import path
from os import mkdir
import commands
import socket
import fcntl
import struct
import array
import halib.Logger as logger
import halib.chaif.SanityCheck as sanity

logger.section("HAOSCAR configurator running...")

logger.subsection("please ensure you are running as root")
#Some comments
db_comment = """\n#HA_DB_TYPE specifies the type of database that will be
#created when the database initialization routines start.
#DB_UNAME specifies the username of the database to be setup
#DB_PASS specifies the password of the database to be setup\n"""
nic_comment = """\n#NIC_INFO specifies which network interface card will
#be used. It is essential that this information is correct since heartbeat
#signals will be setup on this.\n"""
file_comment = """\n#DATA_DIR specifies the device name of the 
#partition to be synchronized. Typically home file system partition
#if DRBD is to be used and the partition scheme is good\n"""
service_comment = """\n#SERVICES specifies the list of services that will be
#monitored by HA-OSCAR. Refer to documentation on how to add more services
#to this list.\n"""
ip_comment = """\n#IP_ADDR specifies the ip_address of the a specific network
#interface.\n"""
intro_comment = "#"*70+"\nAuto generated configuration file, dont change unless you know what you are doing\n"+"#"*70

conf_values = list()

conf_values.append(intro_comment)

#First of all, we check if the directory conf directory exists
CONF_FILE = '/etc/haoscar/haoscar.conf'
if(path.isdir('/etc/haoscar/')):
	logger.subsection("/etc/haoscar is a valid dir")
	if(path.isfile('/etc/haoscar/haoscar.conf')):
		logger.subsection("deleting pre-existing haoscar configuration file")
		commands.getoutput("rm -rf /etc/haoscar/haoscar.conf")
	else:
		logger.subsection("configuration file does not exist, generating one...")
else:
	logger.subsection("creating and generating necessary files")
	mkdir("/etc/haoscar/")

#Now is time to start populating our configuration file with data

########################################################################
str_value = ""
#this currently works only on systems with the by-label defined(most redhatbased)
cmd_output = commands.getoutput("ls /dev/disk/by-label")
if ("home" in cmd_output):
	logger.subsection("the file system home has a label :)")
	conf_values.append(file_comment)
	str_value = "DATA_DIR="+commands.getoutput("findfs LABEL=/home")
	conf_values.append(str_value)
else:
	logger.subsection("could not find home partition label")
	str_value  = raw_input("Enter the device identificaton of your data partition example /dev/sda0 for scsi disks or /dev/hd[e|a]0 for ide: ")
	#Do basic error checking to make sure that is a valid device
	logger.subsection("is "+str_value+" a valid device?")
	cmd_result = commands.getoutput("e2label "+str_value)
	if('superblock' in cmd_result):
		logger.subsection("nope, invalid device, skipping for now")
		conf_values.append(file_comment)
		conf_values.append("#DATA_DIR=")
	else:
		logger.subsection("yep, congratulations we can proceed...")
		conf_values.append(file_comment)
		value = "DATA_DIR="+str_value
		conf_values.append(value)

conf_values.append("\n\n")

#######################################################################
#We move on to network stuffs
conf_values.append(nic_comment)
#This code extracts the list of active interfaces for display to admin
max_possible = 128 #Max no of interfaces, I dont think it ever reaches 128
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
	conf_values.append("NIC_INFO="+interface_list[0])
else:
	temp = ""
	for i in interface_list:
		 temp = temp + i + ", "
	logger.subsection("Detected multiple active interfaces: "+temp)
	str_value = raw_input("Select a network interface from the options above: ")
	cmd_result = commands.getoutput("ifconfig "+str_value)
	if ('error fetching' in cmd_result):
		logger.subsection("invalid device specified, skipping for now")
		conf_values.append("#NIC_INFO=")
	else:
		logger.subsection("adding interface to config file, proceeding...")
		conf_values.append("NIC_INFO="+str_value)
	
	conf_values.append("\n\n")
	logger.subsection("adding ip address of associated interface...")
	ip_addr = socket.inet_ntoa(fcntl.ioctl(
					s.fileno(),
					0x8915,
					struct.pack('256s', str_value[:15])
					)[20:24])
	conf_values.append(ip_comment)
	conf_values.append("IP_ADDR="+ip_addr)
conf_values.append("\n\n")

########################################################################
#We finally provide a default list of services to be monitored 'ssh daemon' really

logger.subsection("generating list of 'default' highly available services")
conf_values.append(service_comment)
conf_values.append("SERVICES={sshd}")

conf_values.append("\n\n")

#######################################################################
#Finally, we describe the type of database to be created by our database
#abstraction method.
conf_values.append(db_comment)

conf_values.append("HA_DB_TYPE=mysql")

uname = raw_input("Enter database username(only alpha numeric passwords): ")
passwd = raw_input("Enter database password(warning input not hashed): ")

conf_values.append("\nDB_UNAME="+uname+"\n")
conf_values.append("DB_PASS="+passwd+"\n")
logger.subsection("adding database configuration info")
conf_values.append("\n\n")

#######################################################################

logger.subsection("finished generating configuration...")

logger.subsection("configuration is now being written to disk")

FILE = open("/etc/haoscar/haoscar.conf","w")

#FILE.writelines(conf_values)

for line in conf_values:
	FILE.writelines(line)

FILE.close()

