# stdlib
import os

# artisan
from server import Server
from observer import Observer
from builder import Builder


#
# Artisan Class. The engine that builds and syncs assets
#
class Artisan(object):

	#
	# Setup - Merge Options
	#
	def __init__(self, src, dest, port, creds):

		# Set instance vars
		self.src = src
		self.dest = dest
		self.port = port
		self.creds = creds


	#
	# Serve files for quick preview
	#
	def craft(self):
		observer = Observer(self.src, self.dest)
		server = Server(self.dest, self.port)


	#
	# Serve files for quick preview
	#
	def ship(self):

		# New artisan
		artisan = Artisan('cloud', src, dest, creds)
		artisan.build()