#! /usr/bin/env python
#
# Copyright (c) 2009 Himanshu Chhetri <himanshuchhetri@gmail.com>        
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

import DatabaseDriver
from os import path
import unittest

class TestSequenceFunctions(unittest.TestCase):

  def setUp(self):
    self.db_path = "/tmp/db"
    self.schema_path = "/usr/share/haoscar/schema.sql"
    self.db = DatabaseDriver.DbDriver(self.db_path, self.schema_path)

  # Test Database was created successfully
  def test_create_database(self):
    self.db.create_database()
    self.assert_(path.exists(self.db_path))

  # Test get_tables method works 
  def test_get_tables(self):
    result = []
    result = self.db.get_tables()
    self.assertEqual(result, ["hainfo"])

  # Test Insert method works properly
  def test_insert(self):
    self.db.insert_db("hainfo", {'os':'linux'})

  # Test Select method works properly
  def test_select(self):
    self.assertEqual({'os':'linux'}, self.db.select_db('hainfo', 'os'))

  # Test Update method works properly
  def test_update(self):
    self.db.update_db('hainfo', {'os':'windows'})
    self.assertEqual({'os':'windows'}, self.db.select_db('hainfo', 'os'))

if __name__ == '__main__':
  unittest.main()
