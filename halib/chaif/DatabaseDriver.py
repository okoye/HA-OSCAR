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
import halib.Logger as logger

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
      logger.subsection("Cannot access database schema file")
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
      logger.subsection("Invalid SQL syntax")
      logger.subsection("Query was :") 
      logger.subsection(query)
      exit(2)
    conn.commit()
    c.close()

# Returns list of tables in database as a list
  def get_tables(self):
    if not path.exists(self.db_path):
      logger.subsection("Cannot access database file at "+ self.db_path)
      exit(2)

    conn = sqlite3.connect(self.db_path)
    c = conn.cursor()
    query = "select name from sqlite_master where type='table'"

    try:
      c.execute(query)
    except:
      logger.subsection("Invalid SQL syntax")
      logger.subsection("Query was :")
      logger.subsection(query)
      exit(2)
    result = []
    for row in c:
      result.append(row[0])  
    c.close()
    return result


# Returns dictionary of key-value pair if key exists in given table of database
  def select_db(self, table, key):
    if not path.exists(self.db_path):
      logger.subsection("Cannot access database file at "+ self.db_path)
      exit(2)
    
    existing_tables = []
    existing_tables = self.get_tables()
    if table not in existing_tables:
      logger.subsection(table+ " does not exist in database")
      exit(2)

    if type(key)!=str or type(table)!=str:
      logger.subsection(key+" "+table+" both must of type String")
      exit(2)

    conn = sqlite3.connect(self.db_path)
    c = conn.cursor()
    query = "SELECT * from %s WHERE name = '%s'" % (table, key)

    try:
      c.execute(query)
    except:
      logger.subsection("Invalid SQL syntax")
      logger.subsection("Query was :") 
      logger.subsection(query)
      exit(2)
    result = {}
    for row in c:
      result[row[0]] = row[1]
    c.close()
    return result


  # Insert given list into given table of database
  def insert_db(self, table, get_dict):
    if not path.exists(self.db_path):
      logger.subsection("Cannot access database")
      exit(2)

    existing_tables = []
    existing_tables = self.get_tables()
    if table not in existing_tables:
      logger.subsection(table+ " does not exist in database")
      exit(2)

    conn = sqlite3.connect(self.db_path)
    c = conn.cursor()

    #Set up the string for insertion
    #TODO: Include an input sanitization method to 'silence' special chars
    query = "INSERT INTO "+table+" ("
    for key in get_dict.keys(): #Possible error source if keys
       query += key              #are retrieved differently each time.
       query += ","
    query = query.rstrip(',')
    query += ") VALUES ("
    for key in get_dict.keys():
      query += get_dict[key]
      query += ","
    query = query.rstrip(',')
    query += ")"

    try:
       c.execute(query)
    except:
      logger.subsection("Invalid SQL syntax")
      logger.subsection("Query was :") 
      logger.subsection(query)
      exit(2)
    conn.commit()
    c.close()

  # Update given table with new dictionary key-value pair
  def update_db(self, table, get_dict):
    if not path.exists(self.db_path):
      logger.subsection("Cannot access database")
      exit(2)

    if type(get_dict) != dict:
      logger.subsection(get_dict+ " must be of type Dictionary")
      exit(2)

    k = get_dict.keys()[0]
    v = get_dict.values()[0]

    if type(k)!=str or type(v)!=str:
      logger.subsection("Dictionary key and value must be of type String")
      exit(2)

    existing_tables = []
    existing_tables = self.get_tables()
    if table not in existing_tables:
      logger.subsection(table+ " does not exist in database")
      exit(2)

    conn = sqlite3.connect(self.db_path)
    c = conn.cursor()
    query = "UPDATE '%s' SET value = '%s' WHERE name = '%s'" % (table, v, k)
    try:
      c.execute(query)
    except:
      logger.subsection("Invalid SQL syntax")
      logger.subsection("Query was :")
      logger.subsection(query)
      exit(2)
    conn.commit()
    c.close()

