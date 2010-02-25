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
from os import path
from os import system
import halib.Exit as exit

init_comment = """\n#HA-OSCAR auto generated monit configuration"""


###################################################
#Handles all initial setup for Monit
###################################################
def configure():
  # Set setup=1 in /etc/default/monit
  data_to_write = ""
  target_file = "/etc/default/monit"
  FILE = open(target_file, "r")

  try:
    for line in FILE:
      if "startup=0" in line:
        data_to_write += "startup=1\n"
      else:
        data_to_write += line
    FILE.close()
  except IOError:
    exit.open("could not write to mon-it config file")

  FILE2 = open(target_file, "w")
  FILE2.write(data_to_write)
  FILE2.close()

 #Configure each component for Mon-IT
  ss
