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

import sys
import commands
import halib.Logger as logger
import halib.chaif.DatabaseDriver as ddriver
from os import path
from os import system

init_comment = """\n#HA-OSCAR auto generated heartbeat authentication
#file. You can change these values but ensure that the file remains
#consistent on the primary and secondary server\n"""

auth_config = "\nauth 2\n2 sha1 changeDefaultPassword\n"
hacf_config = "\nlogfile /var/log/haoscar/heartbeat.log\nlogfacility local0\nkeepalive 2\ndeadtime 30\ninitdead 120\n"


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
		#Eventually, these values should be extracted from the ha database
		auth_value.append(auth_config)
		FILE = open(auth,"w")
		FILE.writelines(auth_value)
		system("chmod 600 /etc/ha.d/authkeys")

	hacf = "/etc/ha.d/ha.cf"
	if(path.isfile(hacf)):
		logger.subsection("ha.cf file already exists, re-writing")
	hacf_value = []
	hacf_value.append(init_comment)
	logger.subsection("auto generating heartbeat configuration file")
	hacf_value.append(hacf_config)
		
	#We need to get the default interface from haoscar.conf
	FILE =  open("/etc/haoscar/haoscar.conf", "r")
	line = FILE.readline()
	while("NIC_INFO=" not in line):
		line = FILE.readline()
	temp = line.split("=")
	if(len(temp)):
		temp = temp[1].lstrip('\n')
		logger.subsection("using interface "+temp)
		hacf_value.append("bcast "+temp)
		hacf_value.append("udpport 694\nauto_failback on\n")
		hacf_value.append("node "+commands.getoutput("uname -n")+"\n")
			
		db_result = ddriver.select_db("Heartbeat","secondary_host")
		if(db_result):
			if(db_result['secondary_host']):
				hacf_value.append("node "+db_result['secondary_host']+"\n")
				FILE = open(hacf, "w")
				FILE.writelines(hacf_value)
				FILE.close()
	else:
		logger.subsection("a fatal error has occured in parsing interface information")
		return 1
	
	haresources = "/etc/ha.d/haresources"
	if(path.isfile(haresources)):
		logger.subsection("haresource configuration exists, skipping")
	else:
		logger.subsection("writing haresource configuration")
		FILE = open("/etc/haoscar/haoscar.conf", "r")
		line = FILE.readline()
		while("IP_ADDR=" not in line):
			line = FILE.readline()
		temp = line.split("=")
		if(len(temp)>1):
			haresource = []
			haresource.append(commands.getoutput("uname -n") + " "+ temp[1])
			FILE = open("/etc/ha.d/haresources","w")
			FILE.writelines(haresource)
		else:
			logger.subsection("a fatal error has occured in parsing ip information")
			return 1

	#If we have not yet died at this point we can assume the configuration was
	#a success
	system("/etc/init.d/heartbeat restart")
	return 0
