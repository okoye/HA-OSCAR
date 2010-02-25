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
import halib.chaif.DatabaseDriver as database
from os import path
from os import system
import halib.Exit as exit
import halib.Logger as logger

init_comment = """\n#HA-OSCAR auto generated config
#file."""
rsync_conf = []

#@des: Responsible for the configuration of the rsync tool. It configures the
#      files found in /etc/rsync.conf automatically and backs up existing
#      ones to /etc/rsync.bak
def configure(secondary=False, configuration=None):
   #Does a file pre-exist?
   rsync_conf_path = "/etc/rsyncd.conf"
   if(path.isfile(rsync_conf_path)):
      logger.subsection("removing previous rsync configuration file to\
 rsyncd.bak")
      system("mv /etc/rsyncd.conf /etc/rsync.bak")
   logger.subsection("creating new rsync config file")
   
   rsync_conf.append(init_comment+"\n")
   ddriver = database.DbDriver()
   #Setup details for primary server
   if(secondary is False):
      #First we set some global rsync variables
      rsync_conf.append("motd file = /etc/rsyncd.motd\n")
      rsync_conf.append("log file = /var/log/rsyncd.log\n")
      rsync_conf.append("pid file = /var/run/haoscar_rsyncd.pid\n")
      rsync_conf.append("lock file = /var/run/rsync.lock\n")
      
      #Now we start setting up all paths specified in 
      #First retrieve all paths and put in a list
      directory = ddriver.select_db('General_Configuration')
      ip = ddriver.select_db('Secondary_Configuration')

      sync_directory = directory[0]["DATA_DIR"]
      secondary_ip = ip[0]["IP_ADDR"]
      count = 0

      sync_directory = sync_directory.split(';')
      sync_directory.pop() #Last item is void.
      
      for key in sync_directory:
         rsync_conf.append("["+key+"]\n")
         rsync_conf.append("path = "+ key+"\n")
         rsync_conf.append("read only = no\n")
         rsync_conf.append("list = no\n")
         rsync_conf.append("hosts allow = "+ secondary_ip+"\n")
         rsync_conf.append("hosts deny = *\n")
         fp = open(rsync_conf_path, "w")
         fp.writelines(rsync_conf)
         fp.close()
   return 0
