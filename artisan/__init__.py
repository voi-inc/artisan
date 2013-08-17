# stdlib
import os
import time
import json
import argparse

# artisan
from utils import merge
from server import Server
from watcher import Watcher
from builder import Builder


class Artisan(object):
    """
    Read config, and execute specified method, passing all required params.
    """

    def __init__(self):
        # Cache
        self.base_dir = os.getcwd()
        # Open, parse, and close config
        with open(os.path.join(self.base_dir, 'artisan.json'), 'r') as file:
            data = json.load(file)

        # Merge and return
        self.config = merge({"port": 8080}, data)

    def craft(self):
        """
        Starting crafting by setting up a temp server
        and observing file system for changes
        """

        dest = os.path.join(self.base_dir, 'preview')
        src_dir = os.path.join(self.base_dir, 'src')
        watcher = Watcher(src_dir, dest)
        server = Server(dest, self.config["port"])

        # Keep her up and running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            server.shutdown()
            watcher.shutdown()

    def ship(self):
        """
        Sync assets to s3 and create final build templates
        """

        dest = os.path.join(self.base_dir, 'build')
        src_dir = os.path.join(self.base_dir, 'src')
        builder = Builder('cloud', src_dir, dest, self.config["aws"])
        builder.build()


def console():
    """
    Parse arguments and create new Artisan instance
    """

    # Command line parser
    parser = argparse.ArgumentParser(
        description='Start web server using passed directory and port'
    )
    parser.add_argument(
        'method',
        help='directory to serve from',
        type=str,
        choices=['craft', 'ship']
    )
    args = parser.parse_args()

    # Run program
    artisan = Artisan()
    getattr(artisan, args.method)()


# Do not run if imported
if __name__ == '__main__':
    console()
