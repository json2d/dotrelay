import sys
import os
import unittest

# constants for testing
MOD_PATH = os.path.abspath(__file__)
TESTS_PATH = os.path.dirname(MOD_PATH)
ROOT_PATH = os.path.dirname(TESTS_PATH)

# importing /w traditional sys path hack
sys.path.append( ROOT_PATH )
import dotrelay

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

  def test__relay_path(self):

    RELAY_PATH = os.path.join(TESTS_PATH, 'cool_math')
    NESTED_MOD_PATH = os.path.join(RELAY_PATH, 'advanced_math', 'core.py')
    with dotrelay.Radio(NESTED_MOD_PATH) as rad:
      self.assertEquals(rad.relay_path, RELAY_PATH)

unittest.main()