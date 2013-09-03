# stdlib
from multiprocessing import Process
import unittest
import os
import time

# 3rd party
from flexmock import flexmock

# artisan
import artisan.crafter


class CrafterTest(unittest.TestCase):
    """
    Test individual methods in Crafter class.
    """
    base_dir = os.path.join(os.getcwd(), 'tests/emails')

    def test_handler(self):
        # Define the file path that will be used to test
        # create, modify, and remove functionality
        new_file = os.path.join(self.base_dir, 'src/test.html')

        # Run crafter in new process so that we can
        # terminate it after running tests
        def worker():
            # Mock Builder class as init build occurs in
            # crafter init (maybe think about changing this)
            (flexmock(artisan.crafter.Builder)
                .should_receive('build')
                .and_return(None))
            # Create a new crafter instance
            crafter = artisan.crafter.Crafter(self.base_dir)
            # Mock event handler to make sure event is
            # dispatched on appropriate methods
            (flexmock(crafter.handler)
                .should_receive('on_any_event')
                .and_return(None)
                .times(3))
            # Start observing
            crafter.craft()

        # Start crafter in new process
        process = Process(target=worker)
        process.start()

        # File operation methods
        def create():
            with open(new_file, 'w+') as file:
                file.write('test')
        def modify():
            with open(new_file, 'w+') as file:
                file.write('testing')
        def delete():
            os.remove(new_file)

        # Helper functin that adds timer inbetween events
        # in order to handle Observer polling
        def test_operation(operation):
            operation()
            time.sleep(1.5)

        # test operations
        test_operation(create)
        test_operation(modify)
        test_operation(delete)

        # Stop crafter process
        process.terminate()
        process.join()

    def test_alter_message(self):
        # Define the file path that will be used to test
        # if correct build_single method is called
        new_file = os.path.join(self.base_dir, 'src/messages/success/test.html')

        # Run crafter in new process so that we can
        # terminate it after running tests
        def worker():
            # Mock Builder class as init build occurs in
            # crafter init (maybe think about changing this)
            BuilderMock = flexmock(artisan.crafter.Builder)
            (BuilderMock
                .should_receive('build')
                .and_return(None)
                .times(1))
            (BuilderMock
                .should_receive('build_single')
                .with_args(new_file)
                .and_return(None)
                .times(1))
            # Create a new crafter instance
            crafter = artisan.crafter.Crafter(self.base_dir)
            # Start observing
            crafter.craft()

        # Start crafter in new process
        process = Process(target=worker)
        process.start()

        # Create new file in messsage directory
        with open(new_file, 'w+') as file:
            file.write('test')
        # Wait due to Observer polling
        time.sleep(1.5)

        # Clean up by removing file
        os.remove(new_file)

        # Stop crafter process
        process.terminate()
        process.join()

    def test_alter_master(self):
        # Define the file path that will be used to test
        # if correct build method is called
        new_file = os.path.join(self.base_dir, 'src/masters/01/test.html')
        
        # Run crafter in new process so that we can
        # terminate it after running tests
        def worker():
            # Mock Builder class as init build occurs in
            # crafter init (maybe think about changing this)
            BuilderMock = flexmock(artisan.crafter.Builder)
            (BuilderMock
                .should_receive('build')
                .and_return(None)
                .times(2))
            # Create a new crafter instance
            crafter = artisan.crafter.Crafter(self.base_dir)
            # Start observing
            crafter.craft()

        # Start crafter in new process
        process = Process(target=worker)
        process.start()

        # Create new file in messsage directory
        with open(new_file, 'w+') as file:
            file.write('test')
        # Wait due to Observer polling
        time.sleep(1.5)

        # Clean up by removing file
        os.remove(new_file)

        # Stop crafter process
        process.terminate()
        process.join()


def suite():
    """
    Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(CrafterTest))
    return test_suite


# Execute from command line
if __name__ == '__main__':
    unittest.main()