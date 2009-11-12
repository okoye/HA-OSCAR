#! /usr/bin/env python
#
# Copyright (c) 2009 Okoye Chuka <okoye9@gmail.com>
#                    Himanshu CHhetri <himanshuchhetri@gmail.com> 
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

from commands import getoutput 
from os import getenv 

errorsList = []

def initialize():
	rootCheck()
	rubyCheck()
	sshCheck()
	networkCheck()
	osCheck()
	return errorsList

def rootCheck():
	if getoutput("whoami") != "root":
		errorsList.append("Not run as root.")

def rubyCheck():
	if "not found" in getoutput("ruby -v"):
		errorsList.append("Ruby not found.")

def sshCheck():
	remoteRootEnabled = False
	try:
		for line in open("/etc/ssh/sshd_config", "r"):
			line = line.replace(' ','')
			line = line.strip('\n')
 			if line == "PermitRootLoginyes" and "#" not in line:
				remoteRootEnabled = True
		if not remoteRootEnabled:
			errorsList.append("Remote root logins via ssh not enabled")
	except IOError:
		errorsList.append("Cannot access sshd_config")

def networkCheck():
	if "localhost" in getoutput("hostname"):
		errorsList.append("Hostname is localhost")

def osCheck():
	osfound = False
	knownOS = ['fedora', 'centos', 'debian', 'ubuntu', 'rhel']
	for OS in knownOS:
		if OS in getoutput("lsb_release -i").lower():
			osfound = True
			break
	if not osfound : errorsList.append("Unsupported Operating System")
