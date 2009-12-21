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
CREATE TABLE IF NOT EXISTS CONFIG(
	ID integer not null unique primary key,
	HOSTNAME_P VARCHAR(50),
	HOSTNAME_S VARCHAR(50),
	DB_TYPE	VARCHAR(10),
	SERVICES VARCHAR(100),
	IP_ADDR_P  VARCHAR(20),
	IP_ADDR_S VARCHAR(20),
	NIC_INFO_P VARCHAR(5),
	NIC_INFO_S VARCHAR(5),
	DATA_DIR VARCHAR(100),
	DATA_SYNC VARCHAR(50)
);
