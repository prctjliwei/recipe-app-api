"""sample tests
"""

from django.test import SimpleTestCase
from app import calc


class CalcTests(SimpleTestCase):
    """Test the calc module"""
    def test_add_numbers(self):
        """test adding numbers"""
        res = calc.add(5, 6)
        self.assertEqual(11, res)
        

    def test_subtract_numbers(self):
        """Test subtracting numbers"""
        res = calc.subtract(10, 15)
        self.assertEqual(5, res)
      
