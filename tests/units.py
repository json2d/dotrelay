import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) ) # the boilerplate we're actually trying to replace with this lib

import unittest

class TestEverything(unittest.TestCase):

  def test__base(self):
    
    try:
        from cool_math import advanced_math
        advanced_math.sqr(2)

    except ImportError:
        self.fail("basic import from a relayed path failed unexpectedly!")


  def test__context_manager(self):

    try:
        from cool_math import advanced_math_w_context_manager
        advanced_math_w_context_manager.sqr(2)

    except ImportError:
        self.fail("basic import from a relayed path (via context manager strategy) failed unexpectedly!")


unittest.main()