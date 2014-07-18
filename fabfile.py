from fabric.api import local
import sys
import SimpleHTTPServer
import SocketServer
from datetime import datetime


def build():
    local('pelican -s pelicanconf.py')


def regenerate():
    local('pelican -r -s pelicanconf.py')


def serve():
    PORT = 8000

    class AddressReuseTCPServer(SocketServer.TCPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(('', PORT),
                                   SimpleHTTPServer.SimpleHTTPRequestHandler)

    sys.stderr.write('Serving on port {0} ...\n'.format(PORT))
    server.serve_forever()


def preview():
    local('pelican -s publishconf.py')


def publish():
    local('pelican -s publishconf.py')
    local('git add .')
    local('echo git commit -am \'%s\'' % datetime.now())
    local('git push')
