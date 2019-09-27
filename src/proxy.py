#!/usr/bin/env python3

import socket
import ssl
import threading
import logging
import binascii
import click

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_message(dns, query, ca_path):

    server = (dns, 853)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(80)

    ctx = ssl.create_default_context()
    ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    ctx.verify_mode = ssl.CERT_REQUIRED
    ctx.check_hostname = True
    ctx.load_verify_locations(ca_path)

    wrapped_socket = ctx.wrap_socket(sock, server_hostname=dns)
    wrapped_socket.connect(server)
    logger.info("Server peer certificate: %s", str(wrapped_socket.getpeercert()))

    tcp_msg = "\x00".encode() + chr(len(query)).encode() + query
    logger.info("Client request: %s", str(tcp_msg))
    wrapped_socket.send(tcp_msg)
    data = wrapped_socket.recv(1024)
    return data

def thread(data, address, socket, dns, ca_path):

    answer = send_message(dns, data, ca_path)
    if answer:
        logger.info("Server reply: %s", str(answer))
        rcode = binascii.hexlify(answer[:6]).decode("utf-8")
        rcode = rcode[11:]
        if int(rcode, 16) == 1:
            logger.error("Error processing the request, RCODE = %s", rcode)
        else:
            logger.info("Proxy OK, RCODE = %s", rcode)
            return_ans = answer[2:]
            socket.sendto(return_ans, address)
    else:
        logger.warn("Empty reply from server.")

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
    DNS to DNS-over-TLS proxy
    """

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((address, port))
        while True:
            data, address = sock.recvfrom(4096)
            threading.Thread(
                    target=thread,
                    args=(data, address, sock, dns, ca)
            ).start()
    except Exception as e:
        logger.error(e)
    finally:
        sock.close()

if __name__ == "__main__":
    main()
