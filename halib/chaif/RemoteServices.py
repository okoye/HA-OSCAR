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
import commands
import halib.chaif.DatabaseDriver as ddriver
import halib.Logger as logger

#Some globals
conf_path = "/usr/share/haoscar/remote.conf" #Should be stored in ha_db
execute_prefix = "pywrat_execute -c /usr/share/haoscar/remote.conf "
def initialize():
	logger.subsection("generating remote configuration files")
	value = "#HA-OSCAR auto generated file for remote connection \n"
	conf = []
	conf.append(value)
	value = "[DEFAULT]\n"
	conf.append(value)
	#There might be issues with sudo based systems like debian.
	ip = raw_input("Enter the IP or DNS hostname of remote system: ")
	#TODO: Check if it is a valid ip
	conf.append("exec_host = "+ip+"\n")
	conf.append("store_host = %(exec_host)s \n")
	conf.append("debug_level = 2\n")
	conf.append("debug_log = /dev/stdout\n\n[communication]\n")
	conf.append("pre_exec_cmd =  \npost_exec_cmd = \n")
	conf.append("ssh_cmd = /usr/bin/ssh\n")
	#TODO: Setup public, private key for logins
	conf.append("exec_key = \n")
	user = raw_input("Admin username on remote host(read warnings for debian systems): ")
	conf.append("exec_user = "+user+"\n")
	conf.append("exec_socket = \nssh_opts = -c blowfish -q\npre_store_cmd =\npost_store_cmd = \nscp_cmd = /usr/bin/scp\nstore_key = %(exec_key)s\nstore_user = %(exec_user)s\nstore_socket = \nscp_opts = -c blowfish -C -r -q\nrsync_cmd = /usr/bin/rsync\nrsync_opts = -z -L -t -r -q")
	FILE = open(conf_path, "w+")
	for value in conf:
		FILE.write(value)
	FILE.close()
	logger.subsection("finished generating remote configuration files")

def execute(command_to_execute):
	return commands.getoutput(execute_prefix + command_to_execute)

#@des:	Receives a path to a script that is to be executed on remote system
#			It uploads the script, then executes it, returns the output of the 
#			script.
def sExecute(path):	
	print "To be implemented"
