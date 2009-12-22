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

# Creates Database and Table
db_path = "/usr/share/haoscar/hadb"
def initialize():
  # Delete sqlite database file if it already exists
  try:
    unlink(db_path)
  except OSError:
    pass
  conn = sqlite3.connect(db_path)
  c = conn.cursor()
  c.execute('''
  CREATE TABLE hainfo
  (
    name VARCHAR(100),
    value VARCHAR(100)
  )
  ''')
  conn.commit()
  c.close()

# Insert given dictionary value
# Eg: insert_db ("HAConfig", {"OS":"Debian"})
def insert_db(table, get_dict):
  conn = sqlite3.connect(db_path)
  c = conn.cursor()
  for k, v in get_dict.iteritems():
    query = "INSERT INTO " + table + " (name, value) "
    query += "VALUES('%s' , '%s')" % (k, v)
    print ("Debug: query is=> %s" %(query))
    c.execute(query)
  conn.commit()
  c.close()

# Returns a dictionary matching the given key from given table
# Eg: select_db ("HAConfig", "OS") => {'OS': 'Debian'}
def select_db(table, get_key):
  conn = sqlite3.connect(db_path)
  c = conn.cursor()
  result = {}
  query = "SELECT * from %s WHERE name = '%s'" % (table, get_key)
  print query
  c.execute(query) 
  for row in c:
    result[row[0]] = row[1]
  c.close()
  return result

# Updates the value of specified field from given dictionary
# Eg: select_db ("HAConfig", "OS") => {'OS': 'Debian'}
#     update_db ("HAConfig", {"OS" : "Redhat"})
#     select_db ("HAConfig", "OS") => {'OS': 'Redhat'}
def update_db(table, get_dict):
  conn = sqlite3.connect(db_path)
  c = conn.cursor()
  get_key = get_dict.keys()[0]
  get_value = get_dict.values()[0]
  query = "UPDATE '%s' SET value = '%s' WHERE name = '%s'" % (table, get_value, get_key)
  c.execute(query)
  conn.commit()
  c.close()
  c.close()
