# PyVPN
Simple VPN client and server implementations in python by Prashant Anantharaman and Kirtivardhan Rathore.


## Dependencies

```shell
sudo apt-get install python-dev python-scapy
sudo pip install python-pytun pycrypto
```

## Architecture


						        +---------------------------------+
						        |                                 |
						        |   10.10.0.1   VPN Server        |
						        |   Server                        |
						        |                                 |
					    +-------+---------------------------------+--------+
					    |                                                  |
					    |                                                  |
					    |                                                  |
					    |                                                  |
					    |                                                  |
					    |                                                  |
					    |                                                  |
		+---------------v----------------+                                +v-------------------------------+
		|                                |                                |                                |
		|   10.10.0.2  Web Server        |                                |   10.10.0.3   Openssh Server   |
		|   Kiwi                         |                                |   Pa                           |
		|                                |                                |                                |
		|                                |                                |                                |
		+--------------------------------+                                +--------------------------------+





### Tunneling

The clients and the servers have the following artifacts:
1. Clients - leamit0 (tun) interface
2. Clients - UDP socket at a fixed port
3. Servers - leamit0 (tun) interface
4. Servers - UDP socket at a fixed port.

******************************************
+      	    IP   	       	   	 +      	       
|	src : Public IP of server	 |
|	dest : Public IP of host	 |
+--------------------------------------->+
|	UDP Payload			 |
|  	The actual packet		 |
|					 |
+--------------------------------------->+


The flow is something like this:

Client sends a poll to the server. Server sends all the packets meant for the client.
Client reads the packets one at a time from the socket it originally sent the poll from.
It writes the payload to its tunnel. It later reads the packet from the same tunnel.
Client ultimately writes the packet to the kernel.
Kernel reads the raw packet and is fooled into thinking it got a reply !

The server operates by receiving a packet, unwrapping it, figuring out who wants to talk to him and forwarding it.
For the server to behave like a client, it must have the same tunnel architecture as the client has
to handle that side of the functionality.

             +--------------------+                          icmp echo reply                                +-------------------+
             |                    +-----------------------------------------------------------------------> |                   |
             |      server socket |                                                                         | client socket     |
             |                    |        <----------------------------------------------------------------+                   |
       +-----+--------------------+------+                        icmp echo request                  +-----------------------+--+------+
       |                                 |                                                           |                       ^         |
       |                                 |                                                           |                       |         |
       |                                 |                                                           |                       |         | first write to tun
write echo request to other client through kernel                                            socket then writes     read from tun      |
       |                                 |                                                   to kernel                       |         |
       |                                 |                                                   which believes it got a reply   |         |
       |                                 |                                                           |                       |         |
+------v------------+        +-----------v-----+                                             +-------v---------+          +--+---------v-----+
|                   |        |                 |                                             |                 |          |                  |
|  server kernel    |        |     tun0        |                                             |  client kernel  |          |    tun0          |
|                   |        |                 |                                             |                 |          |                  |
+-------------------+        +-----------------+                                             +-----------------+          +------------------+


### Polling


                   +                                           +
                   |  Encrypt(Poll(username, password,         |
                   |  timestamp)                               |
                   |                                           |
                   +------------------------------------------>+
                   |                                           |
                   |                                           |
                   |                                           |
                   |                                           |
                   |                                           |
                   | <-----------------------------------------+
                   |                                           |
                   |           Encrypt(Messages)               |
                   |                                           |
                   |                                           |
                   |                                           |
                   +                                           +


We poll the server to ask if it has any new messages for us. We have the polling method running on a separate thread.


### Authentication

Every time the client polls for messages, the client sends the username, MD5 digest of the password and the current timestamp. The client is supplied the username and password as command line arguments. The client is not given any response if the password is not valid. It would be trivial to add a mechanism to prevent DDOS attacks here though.


### Cryptography

We have a shared secret between clients and servers, and make use of XORs to perform authentication. We add a timestamp to the poll messages, and the server keeps a log of past messages hence preventing replay attacks.


## Running the code

The server has to be a remote static IP. We run ours on a public server on a specific port.

### Client

```shell
sudo python client.py --tun-adr 10.10.0.2 --tun-dstaddr 10.10.0.1 --pw password
```

### Server

```shell
sudo python server.py
```

Our server is present at (prashant.at)[prashant.at].

## Testing the code

We have tested our setup, and guarantee that it works for the following protocols.

- HTTP
- SSH
- ICMP

## License
Copyright 2017 Prashant Anantharaman, Kirtivardhan Rathore

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
