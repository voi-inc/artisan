# stdlib
import os

# artisan
from builder import Builder
from syncer import AwsSyncer


class Shipper(object):
    """
    Sync assets to s3 and create final build templates
    """
    def __init__(self, base_dir, storage):
        self.src_dir = os.path.join(base_dir, 'src')
        self.dest_dir = self.src_dir.replace(os.path.basename(self.src_dir), 'build')
        self.storage = storage

    def ship(self):
    	builder = Builder(self.src_dir, self.dest_dir, AwsSyncer(self.storage))
        builder.build()
