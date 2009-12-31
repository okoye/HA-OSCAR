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
import hashlib
import commands
import halib.Logger as logger
import halib.chaif.DatabaseDriver as ddriver
import halib.Exit as exit
directory = "/usr/share/haoscar/Gather/"
gather_table = "Gather_Modules"

#@desc: Reloads all the gathering modules from their
#       designated directory
def reset():
   #Some globals
   dict_config = dict()
   database_driver = ddriver.DbDriver()

   #First, we attempt to get all Gathering modules in our directory
   if(not os.path.exists(directory)):
      logger.subsection("could not find any modules in our gather directory")
      return False

   #Remove all .pyc and .pyo files
   commands.getoutput("rm "+directory+ "*.pyc")
   files = os.listdir(directory)

   #Clear all previous entries in database
   database_driver.truncate_db(gather_table)
   
   #Now, get information for each module in the directory
   for file in files:
      module = __load_module(file)
      try:
         dict_config = module.open()
         dict_config["FULL_PATH"] = directory+file
         dict_config["STATE"] = "1"
         database_driver.insert_db("Gather_Modules", dict_config)
         logger.subsection("loaded module: "+file)
      except:
         logger.subsection("module "+file+" could not be loaded")
   return True

#@desc: Retrieves all the modules whose state is
#       set to a non zero number
def getActiveModules():
   #Some globals
   config = []
   database_driver = ddriver.DbDriver()
   
   #First, retrieve all modules in gather db
   try:
      config = database_driver.select_db("Gather_Modules")
      #For statement
   except:
      #exit.open("fatal error, failed to load gather modules!")
      pass

   print config
   return config

def getAllModules():
      pass

def removeActiveModules():
      pass

def addActiveModule():
      pass

def __load_module(module):
   code_path = directory + module
   try:
      try:
         code_dir = os.path.dirname(code_path)
         code_file = os.path.basename(code_path)

         fin = open(code_path, 'rb')

         return imp.load_source(hashlib.md5(code_path).hexdigest(), code_path, fin)
      finally:
         try: 
            fin.close()
         except: 
            pass
   except ImportError, x:
      logger.subsection("failed to import "+module)
   except:
      logger.subsection("an unknown import module error has occured.")
