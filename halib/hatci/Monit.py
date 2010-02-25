#! /usr/bin/env python
#
# Copyright (c) 2010 Himanshu Chhetri<himanshuchettri@gmail.com>
#                    Okoye Chuka D. <okoye9@gmail.com>
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
import halib.chaif.DatabaseDriver as database_driver
import halib.hatci.monit.Apache as apache
import halib.hatci.monit.Sshd as ssh
import halib.hatci.monit.Syslog as syslog
from os import path
from os import system
import halib.Exit as exit

init_comment = """\n#HA-OSCAR auto generated Mon-it configuration"""
rules = []

###################################################
#Handles all setup for Monit
###################################################
def configure():
  rules.append(init_comment)
   
  rules.append("\nstartup=1\n")

  #TODO: Make this part automatic.
  #Configure each component for Mon-IT
  #Apache Config:
  logger.subsection("adding apache config")
  rules.append("\n")
  rules.append(apache.configure())

  #Sshd Config:
  logger.subsection("adding sshd config")
  rules.append("\n")
  rules.append(ssh.configure())

  #Syslog Config:
  logger.subsection("adding syslog config")
  rules.append("\n")
  rules.append(syslog.configure())

  #We can now write out to config file
  FILE = open("/etc/default/monit", "w")
  try:
    for line in rules:
      FILE.write(line)
    FILE.close()
  except IOError:
    exit.open("could not write monit rules")

  return 0
