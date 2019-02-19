#! /usr/bin/env python3

import contextlib
import os
import socket
import sys

# ========== Config ===========
MOSH_SERVER = 'mosh-server'
# Path to the mosh-server executable.

BIND_TO_DEFAULT_ADDR = False
# Whether mosh-server should bind to the discovered default address, or bind
# to the wildcard address.

HARDCODED_SERVER_ADDR = None
# If the server IP address is fixed and you would like to have it hardcoded,
# specify it here.

TEST_IPV4_HOST = '8.8.8.8'
# This address is used when detecting the host address towards the default
# route. This should be an address not on any local subnet. No actual traffic
# is sent.

# ==========


def get_default_route_ipv4_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    with contextlib.closing(s):
        s.connect((TEST_IPV4_HOST, 0))
        return s.getsockname()[0]


def main():
    args = sys.argv[1:]

    server_addr = HARDCODED_SERVER_ADDR or get_default_route_ipv4_address()

    # Replace "-s" argument.
    # When invoking mosh without "--bind-servers" or explicitly with
    # "--bind-server=ssh", mosh-server will be invoked with "-s", which tells
    # it to bind to the IP address of the incoming SSH connection. We do not
    # want that, so we will tell mosh-server to bind to the discovered default
    # address instead.
    # This should not prevent other "--bind-servers" arguments from working.
    for i, a in enumerate(args):
        if a == '-s':
            args[i:i+1] = ['-i', server_addr]
            break

    print('MOSH IP {!s}'.format(server_addr))
    os.execvp(MOSH_SERVER, [MOSH_SERVER] + args)


if __name__ == '__main__':
    main()
