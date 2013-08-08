# stdlib
import unittest
import os
import shutil

# module
from artisan.builder import Builder


#
# Builder unit tests
#
class BuilderTest(unittest.TestCase):

    #
    # Setup
    #
    @classmethod
    def setUpClass(self):

        # Graphical Helper
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        print 'BUILDER TEST'
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'

        # init builder
        # self.builder = Builder()

    #
    # Teardown
    #
    @classmethod
    def tearDownClass(self):
        print 'teardown'
        # shutil.rmtree(self.devDir)


    #
    # Build all masters and messages 
    #
    def test_build(self):
        print 'build'


    #
    # Loop over all masters and sync media
    #
    def test_build_masters(self):
        print 'build masters'


    #
    # Loop over all messages and build
    #
    def test_build_messages(self):
        print 'build messages'


    #
    # Build one message
    #
    def test_build_message(self):
        print 'build message'


    #
    # Write
    #
    def test_write(self):
        print 'craft'
        # self.assertTrue(os.path.isfile(filePath))


    # 
    # Sync images
    #
    def test_sync(self):
        print 'sync'

    # 
    # Sync local
    #
    def test_sync_local(self):
        print 'sync local'


    # 
    # Sync cloud
    #
    def test_sync_cloud(self):
        print 'sync cloud'


#
# Gather all the tests from this module in a test suite.
#
def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(BuilderTest))
    return test_suite


# Execute from command line
if __name__ == '__main__':
    unittest.main()