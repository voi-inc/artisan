# stdlib
import unittest
import os

# 3rd party
from flexmock import flexmock

# artisan
import artisan.shipper


class ShipperTest(unittest.TestCase):
    """
    Test individual methods in Shipper class.
    """
    def test_ship(self):
        # Cache paths
        base_dir = os.path.join(os.getcwd(), 'tests/emails')
        src_dir = os.path.join(base_dir, 'src')
        dest_dir = src_dir.replace(os.path.basename(src_dir), 'build')
        # Mock Builder class and make sure it is intilized correctly.
        # Also check to make sure the build method is called 1x.
        BuilderMock = flexmock(artisan.shipper.Builder)
        (BuilderMock.should_call('__init__')
            .with_args(src_dir, dest_dir, object)
            .times(1))
        (BuilderMock.should_receive('build')
            .times(1))
        # Create shipper instance and ship
        shipper = artisan.shipper.Shipper(base_dir, 's')
        shipper.ship()


def suite():
    """
    Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(ShipperTest))
    return test_suite


# Execute from command line
if __name__ == '__main__':
    unittest.main()
