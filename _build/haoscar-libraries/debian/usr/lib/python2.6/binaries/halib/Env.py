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
import halib.Logger as logger

#First, we set home directory to get rid of Debian bug!
os.environ['HAS_HOME'] = os.getcwd()

#There are two cases, in the first case a profile.d file exists which we can 
#update with HAS_HOME but in the second case, profile.d does not exist 
#meaning the script is running on an debian based distro.

def configureEnvironment():
	if os.path.isfile("/etc/redhat-release"):
		logger.subsection("Local system is a redhat based distro")
		logger.subsection("Setting HAS_HOME directory variable to current dir")
		if not os.path.isfile("/etc/profile.d/has_home.csh"): #csh shells
			cwd = os.getcwd()
			cmd4rpm = "setenv HAS_HOME "+cwd
			FILE = open("/etc/profile.d/has_home.csh","w")
			FILE.writelines(cmd4rpm)
			FILE.close()
			os.system("chmod 755 /etc/profile.d/has_home.csh")
		else:
			logger.subsection("It seems HAS_HOME(csh) has been set already, skipping")
		if not os.path.isfile("/etc/profile.d/has_home.sh"): #sh shells
			cwd = os.getcwd()
			cmd4rpm = "HAS_HOME="+cwd+"\n"+"export HAS_HOME"
			FILE = open("/etc/profile.d/has_home.sh", "w")
			FILE.writelines(cmd4rpm)
			FILE.close()
			os.system("chmod 755 /etc/profile.d/has_home.sh")
		else:
			logger.subsection("It seems HAS_HOME(sh) has been set already, skipping")
	else:
		logger.subsection("Local system is a debian based distro")
		logger.subsection("Setting HAS_HOME directory variable to current dir")
		cwd = os.getcwd()
		cmd4deb0 = "echo HAS_HOME="+cwd
		cmd4deb1 = "echo export HAS_HOME >> /root/.bashrc"
		if commands.getoutput("grep HAS_HOME /root/.bashrc"):
			logger.subsection("It seems HAS_HOME has been set already, skipping")
		else:
			os.system(cmd4deb0)
			os.system(cmd4deb1)
