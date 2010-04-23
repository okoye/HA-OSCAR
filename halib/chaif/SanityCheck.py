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

import os
from commands import getoutput 
from os import getenv 

errorsList = []

def initialize():
	rootCheck()
	rubyCheck()
	networkCheck()
	osCheck()
        heartbeatCheck()
        monitCheck()
	return errorsList

def rootCheck():
	if getoutput("whoami") != "root":
		errorsList.append("Not run as root")

def rubyCheck():  #is not failing when it should be.
  if "not found" in getoutput("ruby -v")\
        and "/ruby" not in getoutput("which ruby"):
    errorsList.append("Ruby not found")

#sshCheck is unnecessary
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
  knownOS = ['fedora', 'centos', 'debian', 'ubuntu', 'rhel']
  output = getoutput("lsb_release -is").lower()
  if "not found" in output:
    errorsList.append("LSB information unavailable. Is LSB installed?")
  else:
    if not (output in knownOS): #lsb_release not default in fedora
      errorsList.append("Unsupported operating system")

#TODO: Update these heartbeat, rsync, and monit to check using the
#      package manager of respective distributions
def heartbeatCheck():
   if (not (os.path.exists("/etc/init.d/heartbeat"))):
      errorsList.append("Heartbeat is not installed")

def rsyncCheck():
   if(not (os.path.exists("/usr/bin/rsync"))):
      errorsList.append("Rsync is not installed")

def monitCheck():
   if(not(os.path.exists("/etc/init.d/monit"))):
      errorsList.append("Monit is not installed")
