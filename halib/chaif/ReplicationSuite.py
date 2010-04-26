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
   def clone(self):
      """retrieve all necessary data from db"""
      database = ddriver.DbDriver()
      primary_conf = database.select_db('Primary_Configuration')
      secondary_conf = database.select_db('Secondary_Configuration')
      general_conf = database.select_db('General_Configuration')

      """now set all variables necessary"""
      imager_config = []
      imager_config.append("GROUP_NAME:ha_group\n")
      imager_config.append("HA_ETH:"+primary_conf[0]["NIC_INFO"]+"\n")
      imager_config.append("IMAGE_DIR:/usr/share/haoscar/images\n")
      imager_config.append("IMAGE_NAME:ha_image\n")
      imager_config.append("MASK:"+general_conf[0]["MASK"]+"\n")
      imager_config.append("PRIMARY_HOSTNAME:"+primary_conf[0]["HOSTNAME"]+"\n")
      imager_config.append("PRIMARY_IP:"+primary_conf[0]["IP_ADDR"]+"\n")
      imager_config.append("SECONDARY_HOSTNAME:"\
          +secondary_conf[0]["HOSTNAME"]+"\n")
      imager_config.append("SECONDARY_IP:"+secondary_conf[0]["IP_ADDR"]+"\n")
      imager_config.append("SUBNET:"+general_conf[0]["SUBNET"]+"\n")
      
      #Now we do some writing
      FILE = open("/usr/share/haoscar/sysimager.conf","w")
      for config in imager_config:
         FILE.writelines(config)
      FILE.close()
      logger.subsection("finished configuring sysimager.conf")

      logger.subsection("starting cloning process")
      print commands.getoutput("haoscar-system-clone.sh")
