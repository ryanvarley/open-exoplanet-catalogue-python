"""
Help?
"""
__version__ = '2.0a150616a'


def test():
    import unittest

    from tests import testsuite as _testsuite
    unittest.TextTestRunner(verbosity=2).run(_testsuite)

# OECPy Imports
import sys

# Import package modules
from . import assumptions, astroclasses, astroquantities, equations, example, flags, plots
# import OEC database
from .database import OECDatabase, load_db_from_url
