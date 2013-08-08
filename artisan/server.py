# stdlib
import os
import time
import argparse
import threading
import SocketServer
from SimpleHTTPServer import SimpleHTTPRequestHandler


#
# Serve files in a specified directory on a specified port
#
class Server(object):

	#
	# Setup httpd
	#
	def __init__(self, dir, port):

		# Change cwd and setup http server
		os.chdir(dir)
		self.httpd = SocketServer.TCPServer(("", port), SimpleHTTPRequestHandler, bind_and_activate=False)

		# Prevent 'cannot bind to address' errors on restart
		# Manually bind, to support allow_reuse_address
		self.httpd.allow_reuse_address = True
		self.httpd.server_bind()
		self.httpd.server_activate()

		# Start server in new thread
		self.server_thread = threading.Thread(target=self.worker)
		self.server_thread.daemon = True
		self.server_thread.start()

	#
	# Start server
	#
	def worker(self):
		self.httpd.serve_forever()

	#
	# Stop server
	#
	def shutdown(self):
		self.httpd.shutdown()
		self.server_thread.join()


#
# Run when called from console
#
def console():

	# Command line parser
	parser = argparse.ArgumentParser(description='Start web server using passed directory and port')
	parser.add_argument('--port', '-p', help='port to access served content', type=int, default=8080)
	parser.add_argument('--directory', '-d', help='directory to serve from', type=str, required=True)

	# Parse Start server
	args = parser.parse_args()
	server = Server(args.directory, args.port)

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		server.shutdown()


# Do not run if imported
if __name__ == '__main__':
	console()