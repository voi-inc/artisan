# stdlib
import unittest
import os
import urllib

# module
from artisan.server import Server


#
# Server unit tests
#
class ServerTest(unittest.TestCase):

    # Properties
    PORT = 8080
    serve_dir = os.path.join(os.getcwd(), 'tests/emails')
    test_url = 'http://localhost:8080/artisan.json'

    #
    # Create new server
    #
    @classmethod
    def setUpClass(self):

        # Graphical Helper
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        print 'SERVER TEST'
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'

        # Start Server
        self.server = Server(self.serve_dir, self.PORT)


    #
    # Shutdown server after testing
    #
    @classmethod
    def tearDownClass(self):
        self.server.shutdown()


    #
    # Request and check status code
    #
    def test_server(self):
        status = urllib.urlopen(self.test_url).getcode()
        self.assertEqual(status, 200)

#
# Gather all the tests from this module in a test suite.
#
def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(ServertTest))
    return test_suite


# Execute from command line
if __name__ == '__main__':
    unittest.main()