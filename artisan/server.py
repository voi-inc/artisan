# stdlib
import os
import time
import argparse
import threading
import SocketServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import sys


class Server(object):
    """
    Serve files in a specified directory on a specified port
    """
    def __init__(self, dir, port):
        # Change cwd and setup http server
        os.chdir(dir)
        self.httpd = SocketServer.TCPServer(
            ("", port),
            SimpleHTTPRequestHandler,
            bind_and_activate=False
        )
        # Prevent 'cannot bind to address' errors on restart
        # Manually bind, to support allow_reuse_address
        self.httpd.allow_reuse_address = True
        self.httpd.server_bind()
        self.httpd.server_activate()

        # Start server in new thread
        def worker(self):
            self.httpd.serve_forever()

        self.server_thread = threading.Thread(target=worker)
        self.server_thread.daemon = True
        self.server_thread.start()

    def shutdown(self):
        self.httpd.shutdown()
        self.server_thread.join()


def console():
    """
    Parse arguments and start server daemon
    """
    ret_code = 0

    # Command line parser
    parser = argparse.ArgumentParser(
        description='Start web server using passed directory and port')
    parser.add_argument(
        '--port',
        '-p',
        help='port to access served content',
        type=int,
        default=8080
    )
    parser.add_argument(
        '--directory',
        '-d',
        help='directory to serve from',
        type=str,
        required=True
    )
    # Parse Start server
    args = parser.parse_args()
    server = Server(args.directory, args.port)
    # Keep it running until interrupted
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.shutdown()
        ret_code = 1

    return ret_code


# Do not run if imported
if __name__ == '__main__':
    sys.exit(console())

