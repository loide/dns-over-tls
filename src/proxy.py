#!/usr/bin/env python3

import socket
import ssl
import threading
import logging
import click
import os
from udp import Udp
from tcp import Tcp


def listen_tcp(address, port, dns, ca):
    """ Listening for DNS TCP requests """
    logging.info(
            "LISTENING TCP: %d",
            os.getpid()
            )
    try:
        tcp = Tcp()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((address, port))
        sock.listen(2)
        while True:
            conn, addr = sock.accept()
            data = conn.recv(1024)
            threading.Thread(
                    target=tcp.handler,
                    args=(data, addr, conn, dns, ca)
                    ).start()
    except Exception as e:
        logging.error(e)
    finally:
        sock.close()


def listen_udp(address, port, dns, ca):
    """ Listening for DNS UDP requests """
    logging.info(
            "LISTENING UDP: %d",
            os.getpid()
            )
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
@click.option(
    '-p', '--port', default=53,
    help="Port of the listening proxy [default: 53]"
)
@click.option(
    '-a', '--address', default="0.0.0.0",
    help="Address of the proxy network interface to use \
            [default: 0.0.0.0]"
)
@click.option(
    '-d', '--dns', default="1.1.1.1",
    help="Domain Name Server with TLS support \
            [default: 1.1.1.1]"
)
@click.option(
    '-c', '--ca', default="/etc/ssl/cert.pem",
    help="Path to the root and intermediate certificates file \
            [default: /etc/ssl/cert.pem]"
)
def main(port, address, dns, ca):
    """
    DNS to DNS-over-TLS simple deamon.
    """
    logging.basicConfig(level=logging.INFO)
    threads = []
    p_udp = threading.Thread(target=listen_udp, args=(address, port, dns, ca))
    p_udp.start()
    threads.append(p_udp)

    p_tcp = threading.Thread(target=listen_tcp, args=(address, port, dns, ca))
    p_tcp.start()
    threads.append(p_tcp)

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
