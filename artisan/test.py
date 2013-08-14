# stdlib
import os
import time
import logging

# 3rd party
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import LoggingEventHandler

class Watcher(object):
    """
    Setup and manage watchdog daemon.
    """

    def __init__(self, src, dest):
        # Cache vars
        self.dest = dest
        self.src = src
        # Init handler
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        event_handler = LoggingEventHandler()
        self.observer = Observer()
        self.observer.schedule(event_handler, path=self.src, recursive=True)
        self.observer.start()

    def shutdown(self):
        self.observer.stop()
        self.observer.join()


if __name__ == '__main__':
    watcher = Watcher('/vagrant/tests/emails/src', '/vagrant/tests/emails/preview')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        watcher.shutdown()