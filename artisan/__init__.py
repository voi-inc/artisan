# stdlib
import os
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

    def __init__(self, method):
        # Cache
        self.src = os.path.join(os.getcwd(), 'src')
        # Open, parse, and close config
        file = open(os.path.join(os.getcwd(), 'artisan.json'))
        data = json.load(file)
        file.close()
        # Merge and return
        self.config = merge({"port": 8080}, data)
        # Call passed method
        method = getattr(self, method)
        method()

    def craft(self):
        """
        Starting crafting by setting up a temp server
        and observing file system for changes
        """

        dest = self.src.replace(os.path.basename(self.src), 'preview')
        watcher = Watcher(self.src, dest)
        server = Server(dest, self.port)

    def ship(self):
        """
        Sync assets to s3 and create final build templates
        """

        dest = self.src.replace(os.path.basename(self.src), 'build')
        artisan = Artisan('cloud', self.src, dest, self.aws)
        artisan.build()


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
    artisan = Artisan(args.method)


# Do not run if imported
if __name__ == '__main__':
    console()
