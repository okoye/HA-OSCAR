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
	return errorsList

def rootCheck():
	if getoutput("whoami") != "root":
		errorsList.append("Not run as root")

def rubyCheck():  #is not failing when it should be.
  if "not found" in getoutput("ruby -v")\
        and "/ruby" not in getoutput("which ruby"):
    errorsList.append("Ruby not found")

def networkCheck():
	if "localhost" in getoutput("hostname"):
		errorsList.append("Hostname is localhost")

def osCheck():
  knownOS = ['fedora', 'centos', 'debian', 'ubuntu', 'rhel']
  output = getoutput("lsb_release -is").lower()
  if not (output in knownOS): #lsb_release not default in fedora
    errorsList.append("Unsupported operating system")
