import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) ) # the boilerplate we're actually trying to replace with this lib

import unittest

class TestEverything(unittest.TestCase):

  def test_base(self):
    
    try:
        from cool_math import advanced_math
        advanced_math.sqr(2)

    except ImportError:
        self.fail("basic import from a relayed path failed unexpectedly!")


unittest.main()