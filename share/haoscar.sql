--  HAOSCAR Database Tables
--
--  This program is free software; you can redistribute it and/or modify
--  it under the terms of the GNU General Public License as published by
--  the Free Software Foundation; either version 2 of the License, or
--  (at your option) any later version.

--  This program is distributed in the hope that it will be useful,
--  but WITHOUT ANY WARRANTY; without even the implied warranty of
--  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
--  GNU General Public License for more details.

--  You should have received a copy of the GNU General Public License
--  along with this program; if not, write to the Free Software
--  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307
--  USA

--
-- Copyright (c) 2009	Okoye Chuka D. <okoye9@gmail.com>	
--                    	All rights reserved.

-- System Config Info
CREATE TABLE IF NOT EXISTS Configuration(
	id integer auto_increment not null unique primary key,
	HOSTNAME_P VARCHAR(100),
	HOSTNAME_S VARCHAR(100),
	DB_TYPE	VARCHAR(100),
	SERVICES VARCHAR(100),
	IP_ADDR_P  VARCHAR(100),
	IP_ADDR_S VARCHAR(100),
	NIC_INFO_P VARCHAR(100),
	NIC_INFO_S VARCHAR(100),
	DATA_DIR VARCHAR(100)
)TYPE=INNODB
