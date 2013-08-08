# stdlib
import unittest

# artisan
import artisan_test
import builder_test
import server_test
import watcher_test


#
# Gather all the tests from this package in a test suite.
#
def suite():
	test_suite = unittest.TestSuite()
	test_suite.addTest(artisan.suite())
	test_suite.addTest(builder.suite())
	test_suite.addTest(server.suite())
	test_suite.addTest(watcher.suite())
	return test_suite


# Execute from command line
if __name__ == "__main__":
    TEST_RUNNER = unittest.TextTestRunner()
    TEST_SUITE = suite()
    TEST_RUNNER.run(TEST_SUITE)