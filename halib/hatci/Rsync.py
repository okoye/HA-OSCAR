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
import halib.chaif.DatabaseDriver as ddriver
from os import path
from os import system
import halib.Exit as exit

init_comment = """\n#HA-OSCAR auto generated config
#file."""
rsync_conf = []

#@des: Responsible for the configuration of the rsync tool. It configures the
#      files found in /etc/rsync.conf automatically and backs up existing
#      ones to /etc/rsync.bak
def configure(secondary=False, configuration=None):
   #Does a file pre-exist?
   rsync_conf_path = "/etc/rsyncd.conf"      
   if(os.path.isfile(rsync_conf_path)):
      logger.subsection("removing previous rsync configuration file to\
      rsyncd.bak")
      system("mv /etc/rsyncd.conf /etc/rsync.bak")
   logger.subsection("creating new rsync config file")
   
   rsync_conf.append(init_comment)

   #Setup details for primary server
   if(secondary is False):
      #First we set some global rsync variables
      rsync_conf.append("motd file = /etc/rsyncd.motd")
      rsync_conf.append("log file = /var/log/rsyncd.log")
      rsync_conf.append("pid file = /var/run/haoscar_rsyncd.pid")
      rsync_conf.append("lock file = /var/run/rsync.lock")
      
      #Now we start setting up all paths specified in 
      #First retrieve all paths and put in a list
      sync_directory = ddriver.select_db("DATA_DIR")
      count = 0

      for key, value in sync_directory:
         rsync_conf.append("["+key+"]")
         rsync_conf.append("path = "+ value)
         rsync_conf.append("read only = no")
         rsync_conf.append("list = no")
         rsync_conf.append("hosts allow = "+ IP_ADDR_S)
         rsync_conf.append("hosts deny = *")
         fp = open(rsync_conf_path, "w")
         fp.writelines(rsync_conf)
         fp.close()
   return 0
