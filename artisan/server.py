# stdlib
import os
import argparse
import SimpleHTTPServer
import SocketServer


class Server(object):

	#
	# Setup - Merge Options
	#
	def __init__(self, directory, port):

		# Change cwd and setup http server
		os.chdir(directory)
		Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
		httpd = SocketServer.TCPServer(("", port), Handler)

		# Server now listening
		print 'listening on port: ' + str(port)
		httpd.serve_forever()


if __name__ == '__main__':

	# Setup command line parser
	parser = argparse.ArgumentParser(description='Start web server using passed directory and port')
	parser.add_argument('--port', '-p', help='port to access served content', type=int, default=8080)
	parser.add_argument('--directory', '-d', help='directory to serve from', type=str, required=True)

	# Parse and create new server instance
	args = parser.parse_args()
	server = Server(args.directory, args.port)