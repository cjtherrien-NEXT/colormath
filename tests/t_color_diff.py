"""
 Color Math Module (colormath) 
 Copyright (C) 2009 Gregory Taylor

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
Tests for color difference (Delta E) equations.
"""
import unittest
from colormath.color_objects import *
from colormath.color_exceptions import *
from colormath.color_diff import *

class DeltaE_Tests(unittest.TestCase):
    def setUp(self):
        self.color1 = LabColor(lab_l=0.9, lab_a=16.3, lab_b=-2.22)
        self.color2 = LabColor(lab_l=0.7, lab_a=14.2, lab_b=-1.80)
        
    def test_cie2000_accuracy(self):
        result = self.color1.delta_e(self.color2, mode='cie2000')
        expected = 1.523
        self.assertAlmostEqual(result, expected, 3, 
                "DeltaE CIE2000 formula error. Got %.3f, expected %.3f (diff: %.3f)." % (
                                                        result, expected,
                                                        result - expected))
        
    def test_cie2000_accuracy_2(self):
        """
        Follow a different execution path based on variable values.
        """
        # These values are from ticket 8 in regards to a CIE2000 bug.
        c1 = LabColor(lab_l=32.8911,lab_a=-53.0107,lab_b=-43.3182)
        c2 = LabColor(lab_l=77.1797,lab_a=25.5928,lab_b=17.9412)
        result = c1.delta_e(c2, mode='cie2000')
        expected = 78.772
        self.assertAlmostEqual(result, expected, 3, 
                "DeltaE CIE2000 formula error. Got %.3f, expected %.3f (diff: %.3f)." % (
                                                        result, expected,
                                                        result - expected))
        
    def test_cmc_accuracy(self):
        # Test 2:1
        result = self.color1.delta_e(self.color2, mode='cmc', p1=2, pc=1)
        expected = 1.443
        self.assertAlmostEqual(result, expected, 3, 
                "DeltaE CMC (2:1) formula error. Got %.3f, expected %.3f (diff: %.3f)." % (
                                                        result, expected,
                                                        result - expected))
        
        # Test against 1:1 as well
        result = self.color1.delta_e(self.color2, mode='cmc', p1=1, pc=1)
        expected = 1.482
        self.assertAlmostEqual(result, expected, 3, 
                "DeltaE CMC (1:1) formula error. Got %.3f, expected %.3f (diff: %.3f)." % (
                                                        result, expected,
                                                        result - expected))
        
    def test_cie1976_accuracy(self):
        result = self.color1.delta_e(self.color2, mode='cie1976')
        expected = 2.151
        self.assertAlmostEqual(result, expected, 3, 
                "DeltaE CIE1976 formula error. Got %.3f, expected %.3f (diff: %.3f)." % (
                                                        result, expected,
                                                        result - expected))
        
    def test_cie1994_accuracy_graphic_arts(self):
        result = self.color1.delta_e(self.color2, mode='cie1994')
        expected = 1.249
        self.assertAlmostEqual(result, expected, 3, 
                "DeltaE CIE1994 (graphic arts) formula error. Got %.3f, expected %.3f (diff: %.3f)." % (
                                                        result, expected,
                                                        result - expected))
        
    def test_cie1994_accuracy_textiles(self):
        result = self.color1.delta_e(self.color2, mode='cie1994',
                                     K_1=0.048, K_2=0.014, K_L=2)
        expected = 1.204
        self.assertAlmostEqual(result, expected, 3, 
                "DeltaE CIE1994 (textiles) formula error. Got %.3f, expected %.3f (diff: %.3f)." % (
                                                        result, expected,
                                                        result - expected))
    def test_cie1994_domain_error(self):
        # These values are from ticket 98 in regards to a CIE1995
        # domain error exception being raised.
        c1 = LabColor(lab_l=50, lab_a=0, lab_b=0)
        c2 = LabColor(lab_l=50, lab_a=-1, lab_b=2)
        try:
            result = c1.delta_e(c2, mode='cie1994')
        except ValueError:
            self.fail("DeltaE CIE1994 domain error. See issue 9 in tracker.")
        
        
    def test_invalid_delta_e_arg(self):
        invalid_color = "THIS IS NOT A COLOR!"
        self.assertRaises(InvalidArgument, self.color1.delta_e, 
                          invalid_color)
        
    def test_invalid_delta_e_mode(self):
        self.assertRaises(InvalidDeltaEMode, self.color1.delta_e, 
                          self.color2, mode='blahlbah')
        
if __name__ == '__main__':
    unittest.main()