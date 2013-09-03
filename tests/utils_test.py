# stdlib
from multiprocessing import Process
import unittest
import signal
import time
import os

# artisan
import artisan.utils


class UtilsTest(unittest.TestCase):
    """
    Test individual methods in Utils class.
    """
    def test_each_subdir(self):
        # Cache dir and set expected results
        test_dir = os.path.join(os.getcwd(), 'tests/emails/src/messages')
        expected = [
            ('welcome', os.path.join(test_dir, 'welcome')),
            ('success', os.path.join(test_dir, 'success'))
        ]
        # Call each_tmpl method and check for expected results
        for file_name, file_path in artisan.utils.each_subdir(test_dir):
            i = expected.index((file_name, file_path))
            expected.pop(i)

    def test_each_tmpl(self):
        # Cache dir and set expected results
        test_dir = os.path.join(os.getcwd(), 'tests/emails/src/messages/success')
        expected = [
            ('index.txt', os.path.join(test_dir, 'index.txt')),
            ('index.html', os.path.join(test_dir, 'index.html'))
        ]
        # Call each_tmpl method and check for expected results
        for file_name, file_path in artisan.utils.each_tmpl(test_dir):
            i = expected.index((file_name, file_path))
            expected.pop(i)

    def test_keep_daemon_running(self):
        # Worker process that will runn the keep_daemon_running method
        def worker():
            def on_interrupt():
                self.assertTrue(True)
            artisan.utils.keep_daemon_running(on_interrupt)
        # Start a new process
        process = Process(target=worker)
        process.start()
        # After 3 seconds kill it and wait for it to finish executing
        time.sleep(1)
        os.kill(process.pid, signal.SIGINT)
        process.join()

def suite():
    """
    Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(UtilsTest))
    return test_suite


# Execute from command line
if __name__ == '__main__':
    unittest.main()
