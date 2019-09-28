import socket
import ssl
import logging
import binascii

class Tcp:
    def send_request_tls(self, dns, query, ca_path):
        """ Send request to a secure DNS Server from TCP Socket"""
        server = (dns, 853) # default port for cloudflare

        # tcp socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(100)

        ssl_ctx = ssl.create_default_context()
        ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        ssl_ctx.verify_mode = ssl.CERT_REQUIRED
        ssl_ctx.check_hostname = True
        ssl_ctx.load_verify_locations(ca_path)

        wrapped_socket = ssl_ctx.wrap_socket(sock, server_hostname=dns)
        wrapped_socket.connect(server)

        logging.info("Server peer certificate: %s", str(wrapped_socket.getpeercert()))

        wrapped_socket.sendall(query)
        data = wrapped_socket.recv(1024)

        return data

    def response(self, answer, address, conn):
        if answer:
            logging.info("Server reply: %s", str(answer))
            #rcode = binascii.hexlify(answer[:6]).decode("utf-8")
            rcode = answer[:6].hex()
            rcode = rcode[11:]
            if int(rcode, 16) == 1:
                logging.error("Error processing the request, RCODE = %s", rcode)
            else:
                logging.info("Proxy OK, RCODE = %s", rcode)
                conn.send(answer)
        else:
            logging.warn("Empty reply from server.")

    def handler(self, data, address, conn, dns_addr, ca_path):
        answer = self.send_request_tls(dns_addr, data, ca_path)

        self.response(answer, address, conn)
