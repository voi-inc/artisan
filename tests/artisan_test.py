# stdlib
import unittest

# artisan
import artisan


class ArtisanTest(unittest.TestCase):
    """
    Test individual methods in Artisan class.
    """
    def test_parse(self):
        pass


def suite():
    """
    Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(ArtisanTest))
    return test_suite


# Execute from command line
if __name__ == '__main__':
    unittest.main()
