# stdlib
import unittest
import os
import shutil

# 3rd party
from flexmock import flexmock

# artisan
from artisan.builder import Builder


class BuilderTest(unittest.TestCase):
    """
    Test individual methods in Builder class.
    """
    src_dir = os.path.join(os.getcwd(), 'tests/emails/src')
    dest_dir = os.path.join(os.getcwd(), 'tests/emails/build')

    def test_build_message(self):
        # Cache usefule paths
        message_dir = os.path.join(self.src_dir, 'messages/success')
        # Mock syncer and make sure mirror method is called with the
        # correct arguments
        fake_syncer = flexmock()
        (fake_syncer.should_receive('mirror')
            .with_args(self.src_dir, self.dest_dir, message_dir)
            .times(1))
        # Init builder
        builder = Builder(self.src_dir, self.dest_dir, fake_syncer)
        # Make sure write_template is called once for the html file and
        # once for the txt file
        txt_file = os.path.join(message_dir, 'index.txt')
        html_file = os.path.join(message_dir, 'index.html')
        partial_builder = flexmock(builder)
        (partial_builder.should_receive('write_template')
            .and_return(None)
            .with_args(txt_file)
            .times(1))
        (partial_builder.should_receive('write_template')
            .and_return(None)
            .with_args(html_file)
            .times(1))
        # Begin test by calling build_message method
        builder.build_message(message_dir)

    def test_copy_masters_imgs(self):
        # Mock syncer and make sure mirror method is called 2x with the
        # correct arguments
        images_1_src_dir = message_dir = os.path.join(self.src_dir, 'masters/01')
        images_2_src_dir = message_dir = os.path.join(self.src_dir, 'masters/02')
        fake_syncer = flexmock()
        (fake_syncer.should_receive('mirror')
            .with_args(self.src_dir, self.dest_dir, images_1_src_dir)
            .times(1))
        (fake_syncer.should_receive('mirror')
            .with_args(self.src_dir, self.dest_dir, images_2_src_dir)
            .times(1))
        # Init builder
        builder = Builder(self.src_dir, self.dest_dir, fake_syncer)
        builder.copy_masters_imgs()

    def test_write_template(self):
        # Mock syncer and make sure get_base_url method is called 1x
        fake_syncer = flexmock()
        (fake_syncer.should_receive('get_base_url')
            .and_return('')
            .times(1))
        # New builder and write
        builder = Builder(self.src_dir, self.dest_dir, fake_syncer)
        src_html_file = os.path.join(self.src_dir, 'messages/success/index.html')
        builder.write_template(src_html_file)
        # Check for successfull write
        dest_html_file = os.path.join(self.dest_dir, 'messages/success/index.html')
        self.assertTrue(os.path.isfile(dest_html_file))
        # Clean up
        shutil.rmtree(self.dest_dir)


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
