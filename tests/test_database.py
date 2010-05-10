#! /usr/bin/env python
#
# Copyright (c) 2009 Himanshu Chhetri <himanshuchhetri@gmail.com>
#                    Okoye Chuka <okoye9@gmail.com>
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

#   Unit tests for DatabaseDriver in CHAIF

import sys
sys.path.append("../")
import halib.chaif.DatabaseDriver as ddriver
from os import path
import os
import time
import unittest
import shutil

class TestDBFunctions(unittest.TestCase):

  def setUp(self):
    self.db_path = "/tmp/db"
    self.schema_path = "/tmp/schema.sql"
    shutil.copy("../share/schema.sql",self.schema_path) #makes sure that the schema is up to date.
    self.db = ddriver.DbDriver(self.db_path, self.schema_path)

  # Test Database was created successfully
  def test_create_database(self):
    self.db.create_database()
    self.assert_(path.exists(self.db_path)) #Incomplete test
    modtime = os.stat(self.db_path).st_mtime	#Will check the modification time against current time to verify the file is fresh.
    tdiff = time.time() - modtime
    if tdiff < 0:
      tdiff = tdiff * -1
    self.assert_(tdiff < .5)

  # Test get_tables method works 
  def test_get_tables(self):
    test = ["Primary_Configuration", "Secondary_Configuration", "General_Configuration"]
    result = []
    result = self.db.get_tables()
    numexist = 0
    for table in test:
      if table in result:
        numexist = numexist + 1
    self.assert_(numexist == 3)

   #Test Insert method works properly
  def test_insert(self):
    self.db.insert_db("Primary_Configuration", {"HOSTNAME":"clapper", "NIC_INFO":"0ABCD", "IP_ADDR":"1.2.3.4"})
    self.db.insert_db("Secondary_Configuration", {"HOSTNAME":"tapper", "NIC_INFO":"1ABCD", "IP_ADDR":"1.2.3.5"})
    self.db.insert_db("Secondary_Configuration", {"HOSTNAME":"mapper", "NIC_INFO":"2ABCD", "IP_ADDR":"1.2.3.6"})
    self.db.insert_db("Secondary_Configuration", {"HOSTNAME":"napper", "NIC_INFO":"3ABCD", "IP_ADDR":"1.2.3.7"})
    self.db.insert_db("Secondary_Configuration", {"HOSTNAME":"sapper", "NIC_INFO":"4ABCD", "IP_ADDR":"1.2.3.8"})

  # Test Select method works properly
  def test_select(self):
    self.assertEquals(self.db.select_db("Primary_Configuration"),[{"HOSTNAME":"clapper", "NIC_INFO":"0ABCD","IP_ADDR":"1.2.3.4"}])
    self.assertEquals(self.db.select_db("Secondary_Configuration"),[{"HOSTNAME":"tapper", "NIC_INFO":"1ABCD", "IP_ADDR":"1.2.3.5"},{"HOSTNAME":"mapper", "NIC_INFO":"2ABCD", "IP_ADDR":"1.2.3.6"},{"HOSTNAME":"napper", "NIC_INFO":"3ABCD", "IP_ADDR":"1.2.3.7"},{"HOSTNAME":"sapper", "NIC_INFO":"4ABCD", "IP_ADDR":"1.2.3.8"}])

   #Test Truncate method 
  def test_truncate(self):
    self.db.truncate_db("Secondary_Configuration")

if __name__ == '__main__':
  unittest.main()
