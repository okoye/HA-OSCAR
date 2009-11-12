#! /usr/bin/env python
#
# Copyright (c) 2009 Okoye Chuka <okoye9@gmail.com> 
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

#This is the logger module of the High Availability Solution (HAS). It is
#called by all modules and classes that require some form of log be kept.


#The main header signifying the header of a log file. It should only be called
#by the main installer

from os import path
from os import mkdir
import commands

def initialize():
	filename = "/var/log/haoscar/haoscarlog"
	if (not (path.isdir('/var/log/haoscar'))):
		mkdir("/var/log/haoscar")
	
	FILE = open(filename, "w")
	FILE.writelines("")
	FILE.close()

def section(title = None):
	value = "="*40 + "\n"+ "== "+title+"\n"+"="*40
	filename = "/var/log/haoscar/haoscarlog"
	if(path.isfile(filename)):
		if title is None:
			title = " "
		print value
		#Now write to log file
		FILE = open(filename,"a")
		FILE.write(value+"\n")
		FILE.close()
	else:
		print value
#Subsections can be called by any module
def subsection(title = None):
	filename = "/var/log/haoscar/haoscarlog"
	print "--> ",title
	if(path.isfile(filename)):
		FILE = open(filename,"a")
		FILE.write("--> ")
		FILE.write(title+"\n")
		FILE.close()

