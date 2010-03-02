#! /usr/bin/env python
#
# Copyright (c) 2010 Okoye Chuka D.<okoye9@gmail.com>    
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

from os import path
import commands
import halib.chaif.DatabaseDriver as ddriver
import halib.Logger as logger
import halib.Exit as exit

class ReplicationSuite:
   def __init__(self):
      self.image_directory = "/usr/share/haoscar/images"
      self.interface = ""
      self.image_name = "system_image"

   def clone(self):
      if(not path.exists(self.image_directory)):
         logger.subsection("creating image dir: "+self.image_directory)
         commands.getoutput("mkdir -p "+self.image_directory)

      #Now we prepare the golden client image
      logger.subsection("preparing golden client")
      if("FATAL" in commands.getoutput("si_prepareclient --server\
      192.168.0.1 --quiet"):
         logger.subsection("failed to prepare golden client")
         exit.open("system replication failed")

      #Create actual image
      logger.subsection("getting image")
      output = commands.getoutput("si_getimage --golden-client 192.168.0.1 \
      --image "+self.image_name+" --post-install reboot \
      --exclude "+self.image_directory+" --directory "+self.image_directory\
      +" --ip-assignment static --quiet")
      if ("FATAL" in output):
         logger.subection("failed to create image")
         exit.open("image creation failed")

      logger.subsection("starting systemimager-server-rsyncd service")
      commands.getoutput("service systemimager-server-rsyncd start")

      logger.subsection("making bootserver")
      commands.getoutput("si_makebootserver -f --interface="\
      +self.interface "--localdhcp=y --pxelinux=/usr/lib/syslinux/pxelinux.0")

      logger.subsection("configuring dhcp")




