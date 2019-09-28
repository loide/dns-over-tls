#!/usr/bin/env python3

import socket
import ssl
import threading
import logging
import click
from multiprocessing import Process
from udp import Udp
from config import Config

def listen_udp(address, port, dns, ca):
    """ Listening for DNS UDP requests """
    try:
        udp = Udp()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((address, port))
        while True:
            data, address = sock.recvfrom(4096)
            threading.Thread(
                    target=udp.handler,
                    args=(data, address, sock, dns, ca)
                    ).start()
    except Exception as e:
        logging.error(e)
    finally:
        sock.close()


@click.command()
@click.option('-p', '--port',
        default=53, help="Port of the listening proxy [default: 53]")
@click.option('-a', '--address', default="0.0.0.0",
        help="Address of the proxy network interface to use \
                [default: 0.0.0.0]")
@click.option('-d', '--dns', default="1.1.1.1",
        help="Domain Name Server with TLS support \
                [default: 1.1.1.1]")
@click.option('-c', '--ca', default="/etc/ssl/cert.pem",
        help="Path to the root and intermediate certificates file \
                [default: /etc/ssl/cert.pem]")
def main(port, address, dns, ca):
    """
    DNS to DNS-over-TLS simple deamon.
    """
    logging.basicConfig(level=logging.INFO)
    Process(target=listen_udp(address, port, dns, ca)).start()

if __name__ == "__main__":
    main()
