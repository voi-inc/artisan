# stdlib
import os
import time

# 3rd party
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler

# artisan
from builder import Builder


class Watcher(object):
    """
    Setup and manage watchdog daemon.
    """

    def __init__(self, src, dest):
        # Cache vars
        self.dest = dest
        self.src = src
        # Init handler
        handler = ObserverHandler(self.src, self.dest)
        # New observer class
        self.observer = Observer()
        self.observer.schedule(handler, path=self.src, recursive=True)
        self.observer.start()

    def shutdown(self):
        self.observer.stop()
        self.observer.join()



class ObserverHandler(FileSystemEventHandler):
    """
    Watch for file changes in the src directory and update preview
    directory using Builder class.
    """

    def __init__(self, src, dest):
        # Init super
        super(ObserverHandler, self).__init__()
        # Cache values
        self.src = src
        self.dest = dest
        # New builder
        self.builder = Builder('local', self.src, self.dest)
        self.builder.build()

    def dispatch(self, event):
        # Modified to not dispatch create
        if event.event_type != 'created':
            self.on_any_event(event)
        # Dispatch to individual listeners
        _method_map = {
            'modified': self.on_modified,
            'moved': self.on_moved,
            'created': self.on_created,
            'deleted': self.on_deleted,
        }
        _method_map[event.event_type](event)

    def on_any_event(self, event):
        # Build single or build all depending on location of modified file.
        base_dir = self.get_base_dir(event.src_path)
        if base_dir == 'messages':
            self.builder.build_message(event.src_path)
        else:
            self.builder.build()

    def get_base_dir(self, path):
        # Helper method to return parent directory - either master or message.
        path = path.replace(self.src, '')
        #return path.split('/')[1]


# Do not run if imported
if __name__ == '__main__':
    console()
