# stdlib
import os
import json
import argparse

# artisan
from utils import merge
from server import Server
from watcher import Watcher
from builder import Builder

#
# Artisan Class. The engine that builds and syncs assets
#
class Artisan(object):

	#
	# Get config data on init
	#
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


	#
	# Starting crafting by setting up a temp server
	# and observing file system for changes
	#
	def craft(self):
		dest = self.src.replace(os.path.basename(self.src), 'preview')
		watcher = Watcher(self.src, dest)
		server = Server(dest, self.port)

	#
	# Sync assets to s3 and create final build templates
	#
	def ship(self):
		dest = self.src.replace(os.path.basename(self.src), 'build')
		artisan = Artisan('cloud', self.src, dest, self.aws)
		artisan.build()


#
# Run when called from console
#
def console():

	# Command line parser
	parser = argparse.ArgumentParser(description='Start web server using passed directory and port')
	parser.add_argument('method', help='directory to serve from', type=str, choices=['craft', 'ship'])
	args = parser.parse_args()

	# Run program
	artisan = Artisan(args.method)


# Do not run if imported
if __name__ == '__main__':
	console()