# DNS to DNS over TLS proxy

Simple proxy that captures DNS requests from the host, redirects the query over
an encrypted channel to a DNS server that supports TLS (Cloudflare).

Overview

   --------------------           -------------------------        -------------
  | client originating |         | Simple Deamon listen to |       |  DNS/TLS   |
  |     DNS requests   |  <----> | DNS tcp/53 and udp/53   | <---> |   Server   |
  |    conventionally  |         | and establish DNS/TLS   |       |(Cloudflare)|
   --------------------          --------------------------        -------------

## Requirements
* Python3
* Docker

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
  ```


## Testing

