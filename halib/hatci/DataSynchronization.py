#! /usr/bin/env python
#
# Copyright (c) 2008 Louisiana Tech University Research Foundation.  
#                    Chokchai (Box) Leangsuksun <box@latech.edu>
#                    Okoye Chuka D.<okoye9@gmail.com> 
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
import halib.chaif.DatabaseDriver as ddriver
from os import path
from os import system

init_comment = """\n#HA-OSCAR auto generated CSYNC config
#file. You can change these values but ensure that the file remains
#consistent on the primary and secondary server\n"""
csync_conf = []

def configure():
	#Does a file pre-exist?
	cysnc_conf_path = ""
	logger.subsection("creating CSYNC config file")


