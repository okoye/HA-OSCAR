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


from os import path
from sys import exit
import MySQLdb

# Internal method that parses mysql credentials from haoscar.conf
def get_credentials():
  for line in open("/etc/haoscar/haoscar.conf"):
    ar = line.split("=")
    if ar[0].strip() == "DB_UNAME":
      username = ar[1].strip()
    if ar[0].strip() == "DB_PASS":
      password = ar[1].strip()
  return username, password

# Creates database and required tables if they don't exist
def create_db():
  username, password = get_credentials()
  conn = MySQLdb.connect (host = "localhost",
                          user = username, 
                          passwd = password)
  cursor = conn.cursor()
  cursor.execute ("""
  CREATE DATABASE IF NOT EXISTS hadb
  """)
  conn.commit()
  conn.close()


  conn = MySQLdb.connect (host = "localhost",
                          user = username, 
                          passwd = password,
                          db = "hadb")
  cursor = conn.cursor()
  cursor.execute ("""
  CREATE TABLE IF NOT EXISTS Heartbeat
  (
    name VARCHAR(100),
    value VARCHAR(100)
  )
  """)
  cursor.execute ("""
  CREATE TABLE IF NOT EXISTS Secondary_Info
  (
    name VARCHAR(100),
    value VARCHAR(100)
  )
  """)
  conn.commit()
  conn.close()

# Insert value into the specified name of field and table
# Eg: insert_db ("HAConfig", "OS", "Debian")
def insert_db(table, get_name, get_value):
  username, password = get_credentials()
  conn = MySQLdb.connect (host = "localhost",
                          user = username, 
                          passwd = password,
                          db = "hadb")
  cursor = conn.cursor()
  query = "INSERT INTO " + table + " (name, value) "
  query += "VALUES('%s' , '%s')" % (get_name, get_value)
  cursor.execute(query)
  conn.commit()
  conn.close()

# Returns a hash matchig the specified table and field name
# Eg: select_db ("HAConfig", "OS") => {'OS': 'Debian'}
def select_db(table, get_name):
  result = {}
  username, password = get_credentials()
  conn = MySQLdb.connect (host = "localhost",
                          user = username, 
                          passwd = password,
                          db = "hadb")
  cursor = conn.cursor()
  query = "SELECT name, value from %s" % (table)
  cursor.execute(query)
  result_set = cursor.fetchall ()
  for row in result_set:
    if row[0] == get_name:
      result[row[0]] = row[1]

  conn.commit()
  conn.close()
  return result

# Updates the value of specified field name in the given table
# Eg: update_db ("HAConfig", "OS", "Redhat")
def update_db(table, get_name, get_value):
  result = {}
  username, password = get_credentials()
  conn = MySQLdb.connect (host = "localhost",
                          user = username, 
                          passwd = password,
                          db = "hadb")
  cursor = conn.cursor()
  query = "UPDATE %s SET value = '%s' WHERE name = '%s'" % (table, get_value, get_name)
  cursor.execute(query)
  conn.commit()
  conn.close()
