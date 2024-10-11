import argparse
import socket


soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

data, address = soc.recvfrom()
soc.sendto("Hi".encode(), ("128.105.37.222", 20000));

parser = argparse.ArgumentParser(prog='sender',description='sets up a file packet sender on specified port')

parser.add_argument('-p', '--port')           #port is the port on which the sender waits for requests
parser.add_argument('-g', '--requester_port') #requester port is the port on which the requester is waiting
parser.add_argument('-r', '--rate')           #rate is the number of packets to be sent per second
parser.add_argument('-q', '--seq_no')         #seq_no is the initial sequence of the packet exchange
parser.add_argument('-l', '--length')         #length is the length of the payload (in bytes) in the packets

args = parser.parse_args()







