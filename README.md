# DNS to DNS over TLS proxy

Simple proxy that captures DNS requests from the host, redirects the query over
an encrypted channel to a DNS server that supports TLS (Cloudflare). 
It is a deamon that listen to conventional DNS requests on port 53 to capture
DNS UDP and DNS TCP requests.
Runs using multithreading and accept multiples requests.

## Requirements
* Python3
* Docker
* a ssl certificate on /etc/ssl/cert.pem

## Usage
* Running the python script locally:

  After download this repository, install dependencies:

  ```
  $ cd src
  $ pip install -r requirements.txt
  ```
  After this, everything will be all set and you can run:
  ```
  $./proxy --help
  Usage: proxy.py [OPTIONS]

  DNS to DNS-over-TLS simple deamon.

  Options:
    -p, --port INTEGER  Port of the listening proxy [default: 53]
    -a, --address TEXT  Address of the proxy network interface to use
                      [default: 0.0.0.0]
    -d, --dns TEXT      Domain Name Server with TLS support
                      [default: 1.1.1.1]
    -c, --ca TEXT       Path to the root and intermediate certificates file
                      [default: /etc/ssl/cert.pem]
    --help              Show this message and exit.
  ```
* Running in a Docker container:

  On this step, you may build the image using the Dockerfile or just download
  and run the docker image from my Docker Hub account.
  To build and run the docker the docker image:
  ```
  $ docker build -t="dnstls" .
  $ docker run --rm -p 53:53/tcp -p 53:53/udp dnstls
  ```
  To run the image from Docker hub:
  ```
  $ docker run --rm -p 53:53/tcp -p 53:53/udp maraloide/dnstls
  ```

  If instead of using the default dns server or port, you may send a new value
  using the options for proxy.py.

## Testing
  After start the proxy, you can test a DNS request using Dig.
  Query using UDP:
  ```
  $ dig @127.0.0.1 google.com
  ; <<>> DiG 9.10.6 <<>> @127.0.0.1 google.com
  ; (1 server found)
  ;; global options: +cmd
  ;; Got answer:
  ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 25070
  ;; flags: qr rd ra; QUERY: 1, ANSWER: 6, AUTHORITY: 0, ADDITIONAL: 1

  ;; OPT PSEUDOSECTION:
  ; EDNS: version: 0, flags:; udp: 1452
  ; PAD: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 (".....................................................................................................................")
  ;; QUESTION SECTION:
  ;google.com.			IN	A

  ;; ANSWER SECTION:
  google.com.		145	IN	A	64.233.177.101
  google.com.		145	IN	A	64.233.177.102
  google.com.		145	IN	A	64.233.177.113
  google.com.		145	IN	A	64.233.177.138
  google.com.		145	IN	A	64.233.177.139
  google.com.		145	IN	A	64.233.177.100

  ;; Query time: 135 msec
  ;; SERVER: 127.0.0.1#53(127.0.0.1)
  ;; WHEN: Sat Sep 28 21:31:43 EDT 2019
  ;; MSG SIZE  rcvd: 256
  ```
  Query using TCP:
  ```
  $ dig @127.0.0.1 google.com +tcp
  ```

## Concerns & Known issues
* Only tested in Mac OS Mojave.
* Security concerns: this approach gives an additional layer of security, by
sending queries to the DNS server on an encrypted connection. But it is not
protected from the incoming requests from the client which could be attacked
and DNS requests and responses readed or manipulated.
* Should enable Docker Content Trust to verify integrity and authenticity of
the Docker images.
* Vunerable to DNS flood attack

## Improvements
* This proxy could be deployed in a kubernetes cluster to add high availability
and automatic deployment, scaling and load balancing.
* Write and execute more tests (unit and integration).
* Implement support to IPv6
* Check if the input actually is a DNS query and reject if it isn't.
* Support multiples backends and provide some fault tolerance by using the next
if one doesn't answer or fail.
* Implement caching
* Generate and use a proper TLS cert for the handshake
* Save logs to capture the performance
