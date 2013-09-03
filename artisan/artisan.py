# stdlib
import os
import json

# artisan
import utils
from server import Server
from crafter import Crafter
from shipper import Shipper


class Artisan(object):
    """
    Read config, and execute specified method, passing all required params.
    """
    def __init__(self):
        # Cache
        self.base_dir = os.getcwd()
        # Open, parse, and close config
        with open(os.path.join(self.base_dir, 'artisan.json'), 'r') as file:
            self.config = json.load(file)
        # Default port if not supplied
        if not 'port' in self.config.keys():
            self.config['port'] = 8080

    def craft(self):
        """
        Starting crafting by setting up a temp server
        and observing file system for changes
        """
        crafter = Crafter(self.base_dir)
        crafter.craft()
        # Serve
        dest_dir = os.path.join(self.base_dir, 'preview')
        server = Server(dest_dir, self.config['port'])
        server.start()
        # Keep her up and running
        def on_interrupt():
            server.shutdown()
            crafter.shutdown()
        utils.keep_daemon_running(on_interrupt)

    def ship(self):
        """
        Sync assets to s3 and create final build templates
        """
        shipper = Shipper(self.base_dir, self.config['storage'])
        shipper.ship()
