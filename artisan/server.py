# stdlib
import os
import time
import argparse
import threading
import posixpath
import urllib
import SocketServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

# artisan
import utils


class Server(object):
    """
    Serve files in a specified directory on a specified port
    """
    def __init__(self, serv_dir, port):
        # Change cwd and setup http server
        self.httpd = DirTCPServer(
            ("", port),
            RequestHandler,
            bind_and_activate=False,
            serv_dir=serv_dir
        )
        # Prevent 'cannot bind to address' errors on restart
        # Manually bind, to support allow_reuse_address
        self.httpd.allow_reuse_address = True
        self.httpd.server_bind()
        self.httpd.server_activate()

    def start(self):
        # Start server in new thread
        self.server_thread = threading.Thread(target=self.worker)
        self.server_thread.daemon = True
        self.server_thread.start()
        
    def worker(self):
        self.httpd.serve_forever()

    def shutdown(self):
        self.httpd.shutdown()
        self.server_thread.join()


class DirTCPServer(SocketServer.TCPServer):
    """
    Subclass of TCPServer that sets serv_dir
    """
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, serv_dir=os.getcwd()):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        self.serv_dir = serv_dir


class RequestHandler(SimpleHTTPRequestHandler):
    """
    Subclass of SimpleHTTPRequestHandler that servers from
    server.serv_dir rather than os.getcwd() 
    """
    def translate_path(self, path):
        """
        Translate a /-separated PATH to the local filename syntax.
        """

        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = self.server.serv_dir
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path


def console():
    """
    Parse arguments and start server daemon
    """
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
    args = parser.parse_args()

    # Start server and keep it running
    server = Server(args.directory, args.port)
    def on_interrupt():
        server.shutdown()
    utils.keep_daemon_running(on_interrupt)


# Do not run if imported
if __name__ == '__main__':
    console()
