# stdlib
import unittest
import os
import time
import shutil

# 3rd party
from flexmock import flexmock

# artisan
from artisan.builder import Builder


class BuilderTest(unittest.TestCase):
    """
    Test individual methods in Builder class.
    """

    # Properties
    src = os.path.join(os.getcwd(), 'tests/emails/src')
    dest = os.path.join(os.getcwd(), 'tests/emails/build')
    aws = {
        "aws_access_key_id": "id",
        "aws_secret_access_key": "secret",
        "bucket": "email-artisan"
    }

    def setUp(self):
        # Cache vars
        self.success_message = self.create_paths('messages/success')
        self.welcome_message = self.create_paths('messages/welcome')
        self.first_master = self.create_paths('masters/01')
        self.first_master_images = self.create_paths('masters/01/images')
        self.second_master = self.create_paths('masters/02')
        self.second_master_images = self.create_paths('masters/02/images')

    def create_paths(self, str):
        # Convenience fn to create paths and return dict.
        return {
            'src': os.path.join(self.src, str),
            'build': os.path.join(self.dest, str)
        }

    def test_write(self):
        # new builder and write
        src_path = os.path.join(self.success_message['src'], 'index.html')
        builder = Builder('local', self.src, self.dest, self.aws)
        builder.write_template(src_path)
        # check for successfull write
        build_path = os.path.join(self.success_message['build'], 'index.html')
        self.assertTrue(os.path.isfile(build_path))
        # clean up
        shutil.rmtree(self.dest)

    def test_sync(self):
        # Cache img dir
        img_dir = os.path.join(self.success_message['src'], 'images')

        # Test sync with local set
        loc_builder = Builder('local', self.src, self.dest, self.aws)
        (flexmock(loc_builder)
            .should_receive("sync_local")
            .with_args(img_dir)
            .times(1))
        loc_builder.sync(self.success_message['src'])

        # Test sync with cloud set
        cloud_builder = Builder('cloud', self.src, self.dest, self.aws)
        (flexmock(cloud_builder)
            .should_receive("sync_cloud")
            .with_args(img_dir)
            .times(1))
        cloud_builder.sync(self.success_message['src'])

    def test_sync_local(self):
        # Cache img dir
        img_src_dir = os.path.join(self.success_message['src'], 'images')
        img_build_dir = os.path.join(self.success_message['build'], 'images')
        # Test
        builder = Builder('local', self.src, self.dest, self.aws)
        builder.sync_local(img_src_dir)
        # Check for successfull write
        self.assertTrue(os.path.isdir(img_build_dir))
        # clean up
        shutil.rmtree(self.dest)

    def test_sync_cloud(self):
        # TODO (jaridmargolin): Implement fake-s3 for tests
        pass


def suite():
    """
    Gather all the tests from this module in a test suite.
    """

    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(BuilderTest))
    return test_suite


# Execute from command line
if __name__ == '__main__':
    unittest.main()
