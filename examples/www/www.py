# -*- coding: utf-8 -*-
'''
Example using pync to create a single threaded server that
stays open serving the index.html file.
'''

import argparse
import io
import sys

import pync


def main():
    parser = argparse.ArgumentParser('www.py',
            formatter_class=argparse.RawTextHelpFormatter,
            description=__doc__,
    )
    parser.add_argument('dest',
            help='Interface to bind the server to',
            nargs='?',
            metavar='DEST',
            default='',
    )
    parser.add_argument('port',
            help='Port number to bind the server to',
            type=int,
            metavar='PORT',
    )
    args = parser.parse_args()

    # The l option is for listen mode and k for keeping the server open
    # between each client connection.
    try:
        with pync.Netcat(args.port, dest=args.dest,
                l=True, k=True, v=True, q=0) as nc:
            for conn in nc:
                response = io.BytesIO(b'HTTP/1.1 200 OK\n\n')
                conn.readwrite(stdin=response)
                with open('index.html', 'rb') as f:
                    conn.readwrite(stdin=f)
    except KeyboardInterrupt:
        sys.stderr.write('\n')


if __name__ == '__main__':
    main()

