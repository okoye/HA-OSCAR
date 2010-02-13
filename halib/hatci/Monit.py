#! /usr/bin/env python
#
# Copyright (c) 2010 Himanshu Chhetri<okoye9@gmail.com>
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
import sys
import commands
import halib.Logger as logger
import halib.chaif.DatabaseDriver as database_drive
from os import path
from os import system
import halib.Exit as exit

init_comment = """\n#HA-OSCAR auto generated monit configuration"""


###################################################
#Handles all initial setup for Monit
###################################################
def configure():
  # Set setup=1 in /etc/default/monit
  data_to_write = ""
  target_file = "/etc/default/monit"
  FILE = open(target_file, "r")

  try:
    for line in FILE:
      if "startup=0" in line:
        data_to_write += "startup=1\n"
      else:
        data_to_write += line
    FILE.close()
  except IOError:
    errorsList.append("Cannot access " + data_to_write)

  FILE2 = open(target_file, "w")
  FILE2.write(data_to_write)
  FILE2.close()

  services = \
      [ 
          { 
            "header" : 
              [""],
            "group": "",
            "process" : "sshd", "pid" : "/var/run/sshd.pid",
            "group" : "",
            "start" : "/etc/init.d/sshd start",
            "stop" : "/etc/init.d/sshd stop",
            "restarts" : 5, "cycles" : 5,
            "footer" : 
              [
                "if failed port 22 protocol ssh then restart"
              ]
          },

          { 
            "header" : 
              [""],
            "group": "www",
            "process" : "apache", "pid" : "/var/run/httpd.pid",
            "start" : "/etc/init.d/apache start",
            "stop" : "/etc/init.d/apache stop",
            "restarts" : 5, "cycles" : 5,
            "footer" : 
              [
                ""
              ]
          },

          { 
            "header" : 
              [""],
            "group": "",
            "process" : "syslogd", "pid" : "/var/run/syslogd.pid",
            "start" : "/etc/init.d/sysklogd start",
            "stop" : "/etc/init.d/sysklogd stop",
            "restarts" : 5, "cycles" : 5,
            "footer" : 
              [
                "check file syslogd_file with path /var/log/syslog",
                "if timestamp > 65 minutes then alert"
              ]
          },


    ] 

  FILE = open("/etc/monit/monitrc", "a")
  for service in services:
    #print generate_rules(service)
    FILE.write(target)

  FILE.close()
  return 0
# Generate rules for common services
def generate_rules(service):
  header, group, process, pid, start, stop, restarts, cycles, footer= \
      '\n'.join(service["header"]), \
      service["group"], \
      service["process"], \
      service["pid"], \
      service["start"], \
      service["stop"], \
      service["restarts"], \
      service["cycles"], \
      '\n'.join(service["footer"])

  target = "%s\n" % header
  target += "check process %s with pidfile %s\n" % ( process, pid )
  target += "start program  %s\n" % start
  target += "stop program  %s\n" % stop
  target += "if %s restarts within %s cycles then timeout\n" % \
      ( restarts, cycles )
  target += "%s\n" % footer

  return target

