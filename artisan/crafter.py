# stdlib
import os

# 3rd party
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler, DirModifiedEvent

# artisan
from builder import Builder
from syncer import LocalSyncer


class Crafter(object):
    """
    Setup and manage watchdog daemon.
    """
    def __init__(self, base_dir):
        # Cache paths
        src_dir = os.path.join(base_dir, 'src')
        dest_dir = os.path.join(base_dir, 'preview')
        # Init handler
        self.handler = ObserverHandler(src_dir, dest_dir)
        # New observer class
        self.observer = Observer()
        self.observer.schedule(self.handler, path=src_dir, recursive=True)

    def craft(self):
        """
        Start watching src directory
        """
        self.observer.start()

    def shutdown(self):
        """
        Properly shutdown watchdog daemon
        """
        self.observer.stop()
        self.observer.join()


class ObserverHandler(FileSystemEventHandler):
    """
    Watch for file changes in the src directory and update preview
    directory using Builder class.
    """
    def __init__(self, src_dir, dest_dir):
        # Init super
        super(ObserverHandler, self).__init__()
        # Cache values
        self.src_dir = src_dir
        self.dest_dir = dest_dir
        # New builder & local syncer
        self.builder = Builder(self.src_dir, self.dest_dir, LocalSyncer())
        self.builder.build()

    def dispatch(self, event):
        # Modified to not dispatch create
        if not isinstance(event, DirModifiedEvent):
            self.on_any_event(event)
        # Dispatch to individual listeners
        _method_map = {
            'modified': self.on_modified,
            'moved': self.on_moved,
            'deleted': self.on_deleted,
        }
        _method_map[event.event_type](event)

    def on_any_event(self, event):
        # Cache common paths
        abs_path = event.src_path
        rel_path = abs_path.replace(self.src_dir, '')
        # Break path into parts and gether info about parts
        parts = rel_path.strip('/').split('/')
        parts_len = len(parts)

        # Build individual parts of method based on what
        # file/dir was changed:
        def build_message():
            # /message/name
            if (parts_len == 2):
                self.builder.build_single(abs_path)
            # /message/name/file
            # /message/name/images
            elif (parts_len == 3):
                if (parts[2] == 'images'):
                    msg_dir = os.path.dirname(abs_path)
                    self.builder.mirror_imgs(msg_dir)
                else:
                    self.builder.write_template(abs_path)
            # /message/name/images/file
            elif (parts_len == 4):
                img_dir = os.path.dirname(abs_path)
                msg_dir = os.path.dirname(img_dir)
                self.builder.mirror_imgs(msg_dir)  
  
        # If file was deleted remove, else build
        if not os.path.exists(event.src_path):
            self.builder.remove(event.src_path)
        else:
            if parts[0] == 'masters':
                # If an asset in the masters dir was altered
                # we must rebuild everything
                self.builder.build()
            else:
                # Else we just build the part of the message
                # that was changed
                build_message()
