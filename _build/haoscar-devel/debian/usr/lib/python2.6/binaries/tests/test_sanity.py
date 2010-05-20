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

#   Unit tests for SanityCheck in CHAIF

import sys
sys.path.append("../")
import halib.chaif.SanityCheck as sanity
import unittest

class TestSanityFunctions(unittest.TestCase):
  #def setUp(self):
    #I shouldn't need anything.
  
  def test_rootcheck(self):
    sanity.rootCheck()
    self.assert_("Not run as root" not in sanity.errorsList)
    
  def test_rubycheck(self):
    sanity.rubyCheck()
    self.assert_("Ruby not found" not in sanity.errorsList)

  def test_netcheck(self):
    sanity.networkCheck()
    self.assert_("Hostname is localhost" not in sanity.errorsList)

  def test_oscheck(self):
    sanity.osCheck()
    self.assert_("Unsupported Operating System" not in sanity.errorsList)


if __name__ == '__main__':
  unittest.main()
