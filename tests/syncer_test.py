# stdlib
import unittest
import shutil
import os

# artisan
import artisan.syncer


class SyncerTest(unittest.TestCase):
    """
    Test individual methods in Syncer class.
    """
    def test_local_mirror(self):
        base_dir = os.path.join(os.getcwd(), 'tests/emails')
        # Cache img dir
        src_dir = os.path.join(base_dir, 'src')
        img_src_dir = os.path.join(src_dir, 'messages/welcome')
        dest_dir = os.path.join(base_dir, 'build')
        img_dest_dir = os.path.join(dest_dir, 'messages/welcome')
        # Test
        syncer = artisan.syncer.LocalSyncer()
        syncer.mirror(src_dir, dest_dir, img_src_dir)
        # Check for successfull write
        self.assertTrue(os.path.isdir(img_dest_dir))
        # clean up
        shutil.rmtree(dest_dir)

    def test_aws_mirror(self):
        pass
        # TODO (jaridmargolin): Implement fake-s3 for tests

def suite():
    """
    Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(SyncerTest))
    return test_suite


# Execute from command line
if __name__ == '__main__':
    unittest.main()
