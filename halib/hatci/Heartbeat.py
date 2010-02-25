#! /usr/bin/env python
#
# Copyright (c) 2010 Okoye Chuka D.<okoye9@gmail.com>
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
import commands
import getpass
import halib.Logger as logger
import halib.chaif.DatabaseDriver as database_driver
from os import path
from os import system
import halib.Exit as exit

init_comment = """\n#HA-OSCAR auto generated heartbeat authentication
#file. You can change these values but ensure that the file remains
#consistent on the primary and secondary server\n"""

hacf_config = "\nlogfile /var/log/haoscar/heartbeat.log\nlogfacility local0\nkeepalive 2\ndeadtime 30\ninitdead 120\n"

primary_conf = dict()
secondary_conf = dict()

###################################################
#Handles all initial setup for Heartbeat
###################################################
def configure():
	#check if the auth already exists
	auth = "/etc/ha.d/authkeys"	
	if(path.isfile(auth)):
		logger.subsection("authentication configuration already exists, skipping")
	else:   
	 auth_value = []
	 auth_value.append(init_comment)
	 logger.subsection("creating authentication file")
         auth_passwd = getpass.getpass("enter heartbeat authentication passwd: ")
	 auth_value.append("\nauth 2\n2 sha1 ")
         auth_value.append(auth_passwd+"\n")
	 FILE = open(auth,"w+")
	 FILE.writelines(auth_value)
	 system("chmod 600 /etc/ha.d/authkeys")

	hacf = "/etc/ha.d/ha.cf"
	if(path.isfile(hacf)):
		logger.subsection("ha.cf file already exists, re-writing")
	hacf_value = []
	hacf_value.append(init_comment)
	logger.subsection("auto generating heartbeat configuration file")
	hacf_value.append(hacf_config)
	
        #Edited by Chuka Okoye
	#*****ALL References to haoscar.conf need to be re-routed to 
	#*****the HA-OSCAR database 
	#We need to get the default interface from haoscar database
	#FILE =  open("/etc/haoscar/haoscar.conf", "r")
	#line = FILE.readline()
	#while("NIC_INFO=" not in line):
	#	line = FILE.readline()
	#temp = line.split("=")

        ddriver = database_driver.DbDriver() 
	primary_conf = ddriver.select_db('Primary_Configuration')
	secondary_conf = ddriver.select_db('Secondary_Configuration')	
	
	nic_info = ""
	nic_info = primary_conf[0]["NIC_INFO"]
	if(len(nic_info)):
		logger.subsection("using interface "+nic_info)
		hacf_value.append("\nudpport 694 \nbcast "+nic_info)
		hacf_value.append("\nauto_failback on\n")
		hacf_value.append("node "+commands.getoutput("uname -n")+"\n")
			
		if(secondary_conf[0]['HOSTNAME']):
			hacf_value.append("node "+secondary_conf[0]['HOSTNAME']+"\n")
			FILE = open(hacf, "w")
			FILE.writelines(hacf_value)
			FILE.close()
	else:
		logger.subsection("a fatal error has occured: could not retreive interface info")
		return 1
	
	haresources = "/etc/ha.d/haresources"
	if(path.isfile(haresources)):
		logger.subsection("haresource configuration exists, skipping")
	else:
		logger.subsection("writing haresource configuration")

		ip_addr = primary_conf[0]['IP_ADDR']
		if(len(ip_addr)):
			haresource = []
			haresource.append(commands.getoutput("uname -n") + " "+ ip_addr)
			FILE = open("/etc/ha.d/haresources","w")
			FILE.writelines(haresource)
		else:
			logger.subsection("a fatal error has occured, could not retrieve ip information")
			return 1

	#If we have not yet died at this point we can assume the configuration was
	#a success
	return 0
