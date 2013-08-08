# stdlib
import unittest
import os

# module
from artisan.artisan import Artisan


#
# Artisan unit tests
#
class ArtisanTest(unittest.TestCase):

    #
    # Setup
    #
    @classmethod
    def setUpClass(self):

        # Graphical Helper
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        print 'ARTISAN TEST'
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'


    #
    # Teardown
    #
    @classmethod
    def tearDownClass(self):
        print 'teardown'


    #
    # Craft
    #
    def test_craft(self):
        print 'craft'


    #
    # Ship
    #
    def test_ship(self):
        print 'ship'


#
# Gather all the tests from this module in a test suite.
#
def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(ArtisanTest))
    return test_suite


# Execute from command line
if __name__ == '__main__':
    unittest.main()