# stdlib
import unittest
import os
import urllib

# artisan
from artisan.server import Server


class ServerTest(unittest.TestCase):
    """
    Test individual methods in Server class.
    """
    PORT = 8080
    serve_dir = os.path.join(os.getcwd(), 'tests/emails')
    test_url = 'http://localhost:8080/artisan.json'

    def test_server(self):
        # Start server
        self.server = Server(self.serve_dir, self.PORT)
        self.server.start()
        # Request anc check status code
        status = urllib.urlopen(self.test_url).getcode()
        self.assertEqual(status, 200)
        # Stop server daemon
        self.server.shutdown()


def suite():
    """
    Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(ServertTest))
    return test_suite


# Execute from command line
if __name__ == '__main__':
    unittest.main()
