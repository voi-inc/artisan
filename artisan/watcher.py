# stdlib
import os
import time
import argparse
import threading

# 3rd party
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# artisan
from builder import Builder


#
# Watch files and build accordingly
#
class Watcher(object):

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


	#
	# Stop server
	#
	def shutdown(self):
		self.observer.stop()
		self.observer.join()


#
# Event handler that runs build on file system changes
#
class ObserverHandler(FileSystemEventHandler):

	#
	# Init class
	#
	def __init__(self, src, dest):

		# Init super
		super(ObserverHandler, self).__init__()

		# Cache values
		self.src = src
		self.dest = dest

		# New builder
		self.builder = Builder('local', self.src, self.dest)


	#
	# Dispatch to individual event handlers
	#
	def dispatch(self, event):

		# Cache event
		event_type = event.event_type

		# Modified to not dispatch create
		if event_type != 'created':
			self.on_any_event(event)

		# Dispatch to individual listeners
		_method_map = {
			'modified': self.on_modified,
			'moved': self.on_moved,
			'created': self.on_created,
			'deleted': self.on_deleted,
		}
		_method_map[event_type](event)


	#
	# Dispatch to individual event handlers
	#
	def on_any_event(self, event):
		base_dir = self.get_base_dir(event.src_path)
		if base_dir == 'messages':
			self.builder.build_message(event.src_path)
		else:
			self.builder.build()


	#
	# Return base - either master or message
	#
	def get_base_dir(self, path):
		path = path.replace(self.src, '')
		return path.split('/')[1]


#
# Run when called from console
#
def console():

	# Command line parser
	parser = argparse.ArgumentParser(description='Start web server using passed directory and port')
	parser.add_argument('--src', '-s', help='directory to watch', type=str, required=True)
	parser.add_argument('--dest', '-d', help='directory to output build', type=str, required=True)

	# Parse Start server
	args = parser.parse_args()
	watcher = Watcher(args.src, args.dest)

	# Keep up unless interrupted
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		watcher.stop()


# Do not run if imported
if __name__ == '__main__':
	console()