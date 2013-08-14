# stdlib
import unittest
import os
import time

# 3rd party
from flexmock import flexmock

# artisan
import artisan.watcher


class WatcherTest(unittest.TestCase):
    """
    Test individual methods in Watcher class.
    """

    # Properties
    src_dir = os.path.join(
        os.getcwd(),
        'tests/emails/src'
    )
    dest_dir = os.path.join(
        os.getcwd(),
        'tests/emails/build'
    )
    message_file_path = os.path.join(
        os.getcwd(),
        'tests/emails/src/messages/success/test.html'
    )
    master_file_path = os.path.join(
        os.getcwd(),
        'tests/emails/src/masters/01/test.html'
    )

    @classmethod
    def setUpClass(cls):
        # Overwrite Builder class.
        cls.builder = flexmock(TestBuilder)
        artisan.watcher.Builder = TestBuilder
        # Make sure init method is called with proper vars.
        (cls.builder
            .should_receive("__init__")
            .with_args('local', cls.src_dir, cls.dest_dir)
            .times(1))
        # New watcher should be accessible to all test methods.
        cls.watcher = artisan.watcher.Watcher(cls.src_dir, cls.dest_dir)

    @classmethod
    def tearDownClass(cls):
        # Remove created files and stop daemon.
        os.remove(cls.message_file_path)
        os.remove(cls.master_file_path)
        cls.watcher.shutdown()

    def test_messagechange(self):
        # Make sure build_message method is called and passed proper vars.
        (self.builder
            .should_receive("build_message")
            .with_args(self.message_file_path)
            .times(1))
        # Create and close file.
        file = open(self.message_file_path, 'w+')
        file.close()
        # Block with time sleep so watcher has time to trigger fn.
        time.sleep(2)

    def test_masterchange(self):
        # Make sure build method is called and passed proper vars.
        (self.builder
            .should_receive("build")
            .with_args()
            .times(1))
        # Create and close file.
        file = open(self.master_file_path, 'w+')
        file.close()
        # Block with time sleep so watcher has time to trigger fn.
        time.sleep(2)


class TestBuilder(object):
    """
    Gather all the tests from this module in a test suite.
    """

    def __init__(self, type, src, dest):
        pass

    def build(self):
        pass

    def build_message(self, path):
        pass


def suite():
    """
    Gather all the tests from this module in a test suite.
    """

    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(WatcherTest))
    return test_suite


# Execute from command line
if __name__ == '__main__':
    unittest.main()
