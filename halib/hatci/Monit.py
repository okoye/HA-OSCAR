#! /usr/bin/env python
#
# Copyright (c) 2009 Louisiana Tech University Research Foundation.  
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

from lib.chaif.PackageManager import install as pmanager

###################################################
#Handles all initial install and setup for Heartbeat
###################################################
def install():
        #First we attempt to install monit and anyother dependencies
        pmanager('monit')

#def configure():
        #We shall write the default configuration for monit here.

