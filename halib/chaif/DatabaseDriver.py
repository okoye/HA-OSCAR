#! /usr/bin/env python
#
# Copyright (c) 2009 Himanshu CHhetri <himanshuchhetri@gmail.com> 
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


from os import path, unlink
from sys import exit
import sqlite3

class DbDriver:

  def __init__(self, default_db_path = "/usr/share/haoscar/hadb", default_schema_path="/usr/share/haoscar/schema.sql"):
    self.db_path = default_db_path
    self.schema_path = default_schema_path

  def create_database(self):
    # Delete sqlite database file if it already exists
    try:
      unlink(self.db_path)
    except OSError:
      pass

    if not path.exists(self.schema_path):
      print "Cannot access database schema file"
      exit(2)

    # Create database creation query from schema file
    conn = sqlite3.connect(self.db_path)
    c = conn.cursor()
    query = ""
    f = open(self.schema_path)
    for line in f:
      query += line

    try:
      c.execute(query)
    except:
      print "Invalid SQL syntax"
      print "Query was :" 
      print query
      exit(2)
    conn.commit()
    c.close()

# Returns list of tables in database as a list
  def get_tables(self):
    if not path.exists(self.db_path):
      print "Cannot access database file at", self.db_path
      exit(2)

    conn = sqlite3.connect(self.db_path)
    c = conn.cursor()
    query = "select name from sqlite_master where type='table'"

    try:
      c.execute(query)
    except:
      print "Invalid SQL syntax"
      print "Query was :" 
      print query
      exit(2)
    result = []
    for row in c:
      result.append(row[0])  
    c.close()
    return result


  def insert_db(self, table, get_dict):
    if not path.exists(self.db_path):
      print "Cannot access database"
      exit(2)

    k = get_dict.keys()[0]
    v = get_dict.values()[0]

    if not type(k)==str or type(v)==str:
      print "Dictionary key and value must be of type String"
      exit(2)

    existing_tables = []
    existing_tables = self.get_tables()
    if table not in existing_tables:
      print table, "does not exist in database"
      exit(2)

    conn = sqlite3.connect(self.db_path)
    c = conn.cursor()
    query = "INSERT INTO " + table + " (name, value) "
    query += "VALUES('%s' , '%s')" % (k, v)
    try:
      c.execute(query)
    except:
      print "Invalid SQL syntax"
      print "Query was :" 
      print query
      exit(2)
    conn.commit()
    c.close()

