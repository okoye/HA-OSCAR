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
-- Copyright (c) 2010	Okoye Chuka D. <okoye9@gmail.com>	
--                    	All rights reserved.

-- System Config Info
CREATE TABLE Primary_Configuration(
      HOSTNAME text,
      NIC_INFO text,
      IP_ADDR  text,
      FALLBACK_IPS text
);
CREATE TABLE Secondary_Configuration(
      HOSTNAME text,
      NIC_INFO text,
      IP_ADDR text
);
CREATE TABLE General_Configuration(
      DATA_DIR text,
      DATA_SYNC text,
      MASK text,
      SUBNET text
);
CREATE TABLE Gather_Modules(
      COMPONENT text,
      NAME text,
      DESCRIPTION text,
      FULL_PATH text,
      STATE text
);
CREATE TABLE Active_Modules(
      COMPONENT text,
      NAME text,
      DESCRIPTION text,
      FULL_PATH text,
      STATE text
);
