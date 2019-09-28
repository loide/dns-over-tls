import socket
import ssl
import logging
import binascii


class Udp:
    def send_message_tls(self, dns, query, ca_path):
        """ Send request to a secure DNS Server from UDP Socket"""
        try:
            server = (dns, 853)  # default port for cloudflare

            # tcp socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(80)

            ssl_ctx = ssl.create_default_context()
            ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            ssl_ctx.verify_mode = ssl.CERT_REQUIRED
            ssl_ctx.check_hostname = True
            ssl_ctx.load_verify_locations(ca_path)

            wrapped_socket = ssl_ctx.wrap_socket(sock, server_hostname=dns)
            wrapped_socket.connect(server)
            logging.info(
                    "SERVER PEER CERTIFICATE: %s",
                    str(wrapped_socket.getpeercert())
            )

            tcp_msg = "\x00".encode() + chr(len(query)).encode() + query
            logging.info("CLIENT REQUEST: %s", str(tcp_msg))
            wrapped_socket.send(tcp_msg)
            data = wrapped_socket.recv(1024)

            return data

        except Exception as e:
            logging.error(e)
        finally:
            wrapped_socket.close()

    def response(self, answer, address, socket):
        if answer:
            try:
                logging.info("SERVER REPLY: %s", str(answer))
                rcode = binascii.hexlify(answer[:6]).decode("utf-8")
                rcode = rcode[11:]
                if int(rcode, 16) == 1:
                    logging.error(
                            "ERROR PROCESSING THE REQUEST, RCODE = %s",
                            rcode
                    )
                else:
                    logging.info("PROXY OK, RCODE = %s", rcode)
                    return_ans = answer[2:]
                    socket.sendto(return_ans, address)
            except Exception as e:
                logging.error(e)
        else:
            logging.warn("EMPTY REPLY FROM SERVER.")

    def handler(self, data, address, socket, dns_addr, ca_path):
        answer = self.send_message_tls(dns_addr, data, ca_path)

        self.response(answer, address, socket)
