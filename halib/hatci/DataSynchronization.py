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

init_comment = """\n#HA-OSCAR auto generated heartbeat authentication
#file. You can change these values but ensure that the file remains
#consistent on the primary and secondary server\n"""
drbd_conf = []

def configure():
	#Does a file pre-exist?
	drbd_conf_file = "/etc/drbd.conf"
	logger.subsection("creating drbd config file")
	local_drbd_partition = ddriver.select("Configuration", "DATA_DIR_P")
	second_drbd_partition= ddriver.select("Configuration", "DATA_DIR_S")
	p_ip = ddriver.select("Configuration", "IP_ADDR_P")
	s_ip = ddriver.select("Configuration", "IP_ADDR_S")

	drbd_conf.append("global { usage-count no; }")
	drbd_conf.append("resource repdata{")
	drbd_conf.append("protocol C;")
	drbd_conf.append("startup { wfc-timeout 0; degr-wfc-timeout 120; }")
	drbd_conf.append("disk { on-io-error detach; } # or panic,")
	drbd_conf.append("net {  cram-hmac-alg \"sha512\";\n") 
   drbd_conf.append("shared-secret \"r00tf0043v3r\";\n") 
   drbd_conf.append("after-sb-0pri discard-least-changes;\n") 
   drbd_conf.append("after-sb-1pri discard-secondary;\n") 
   drbd_conf.append("after-sb-2pri call-pri-lost-after-sb;\n")
   drbd_conf>append("rr-conflict call-pri-lost;}\n")
	drbd_conf.append(\"syncer { rate 10M; }")

	#local partitioning info

	drbd_conf.append("on drdb1.server {\ndevice /dev/drbd0;")
   drbd_conf.append("disk "+local_drbd_partition["DATA_DIR_P"]+";\n")
   drbd_conf.append("address "+p_ip["IP_ADDR_P"]+":7788;\n")
   drbd_conf.append("meta-disk internal;\n}")
	drbd_conf.append("""on drbd2.server {
	 device /dev/drbd1;""")
	drbd_conf.append("disk "+second_drbd_partition["DATA_DIR_S"]+"; \n")
	drbd_conf.append("address "+s_ip["IP_ADDR_S"]+":7788;\n")
	drbd_conf.append("meta-disk internal; \n}")

	print drbd_conf


