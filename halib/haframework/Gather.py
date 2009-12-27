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
import imp
import commands
import halib.Logger as logger

def reset():
   #First, we attempt to get all Gathering modules in our directory
   directory = "/usr/share/haoscar/Gather/"
   if(not os.path.exists(directory)):
      logger.subsection("could not find any modules in our gather directory")
      return False

   #Remove all .pyc and .pyo files
   commands.getoutput("rm "+directory+ "*.pyc")

   files = os.listdir(directory)

   #Now, get information for each module in the directory
   for file in files:
      module, ext = os.path.splitext(file)
      try:
         fin = open(directory+file,'rb')
         fname = imp.load_source(module,directory+file,fin)
         fname.open
         logger.subsection("adding module "+module)
      except:
         logger.subsection("failed to load "+module)
         
   
   return True
def getActiveModules():
     pass

def getAllModules():
      pass

def removeModules():
      pass

def addModules():
      pass
