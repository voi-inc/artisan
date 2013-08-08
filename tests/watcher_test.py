# stdlib
import unittest
import os
import time

# 3rd party
from flexmock import flexmock

# module
import artisan.watcher


#
# Test Builder Class to Mock
#
class TestBuilder(object):
	def __init__(self, type, src, dest):
		pass
	def build(self):
		pass
	def build_message(self, path):
		pass


#
# Watcher unit tests
#
class WatcherTest(unittest.TestCase):

	# Properties
	src_dir = os.path.join(os.getcwd(), 'tests/emails/src')
	dest_dir = os.path.join(os.getcwd(), 'tests/emails/build')
	message_file_path = os.path.join(os.getcwd(), 'tests/emails/src/messages/test.html')
	master_file_path = os.path.join(os.getcwd(), 'tests/emails/src/masters/test.html')


	#
	# Create new watcher
	#
	@classmethod
	def setUpClass(cls):

		# Graphical Helper
		print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
		print 'WATCHER TEST'
		print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'

		# Overwrite Builder class
		cls.builder = flexmock(TestBuilder)
		artisan.watcher.Builder = TestBuilder

		# Validate init call
		(cls.builder
			.should_receive("__init__")
			.with_args('local', cls.src_dir, cls.dest_dir)
			.times(1)
		)

		# New Watcher
		cls.watcher = artisan.watcher.Watcher(cls.src_dir, cls.dest_dir)


	#
	# Remove build dir (dev)
	#
	@classmethod
	def tearDownClass(cls):
		os.remove(cls.message_file_path)
		os.remove(cls.master_file_path)
		cls.watcher.shutdown()


	#
	# See if build all was triggered
	#
	def test_messagechange(self):

		# Validate build call
		(self.builder
			.should_receive("build_message")
			.with_args(self.message_file_path)
			.times(1)
		)

		# Create and close
		file = open(self.message_file_path, 'w+')
		file.close()

		# Block so watcher can trigger fn
		time.sleep(1)


	#
	# See if build all was triggered
	#
	def test_masterchange(self):

		# Validate build call
		(self.builder
			.should_receive("build")
			.with_args()
			.times(1)
		)

		# Create and close
		file = open(self.master_file_path, 'w+')
		file.close()

		# Block so watcher can trigger fn
		time.sleep(1)


#
# Gather all the tests from this module in a test suite.
#
def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(WatcherTest))
    return test_suite


# Execute from command line
if __name__ == '__main__':
	unittest.main()