import argparse
import socket
import struct

from datetime import datetime
import time

parser = argparse.ArgumentParser(prog='sender',description='sets up a file packet sender on specified port')

parser.add_argument('-p', '--port')           #port is the port on which the sender waits for requests
parser.add_argument('-g', '--requester_port') #requester port is the port on which the requester is waiting
parser.add_argument('-r', '--rate')           #rate is the number of packets to be sent per second
parser.add_argument('-q', '--seq_no')         #seq_no is the initial sequence of the packet exchange
parser.add_argument('-l', '--length')         #length is the length of the payload (in bytes) in the packets

args = parser.parse_args()



soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.bind((socket.gethostbyname(socket.gethostname()), int(args.port)))

req_packet, req_addr = soc.recvfrom(int(args.length) + 9)
req_addr = (req_addr[0], int(args.requester_port))

with open(req_packet[9:].decode(), "rb") as f:
    read_data = f.read()

index = 0
d_size = len(read_data)

sequence = int(args.seq_no)
length = int(args.length)
rate = int(args.rate)

while(index < d_size):
    length = min(d_size - index, length)
    udp_header = struct.pack("!cII", 'D'.encode(), socket.htonl(sequence), length);
    packet = udp_header + read_data[index: index + length]
    soc.sendto(packet, req_addr)

    print("DATA PACKET")
    print("send time:       ", datetime.now().isoformat(sep=" ", timespec="milliseconds"), sep="")
    print("requester addr:  ", req_addr[0], ":", req_addr[1], sep="")
    print("sequence:        ", sequence, sep="")
    print("length:          ", length, sep="")
    print("payload:         ", read_data[index: index + 3].decode(), sep="")
    print()

    index += length
    sequence += length
    time.sleep(1/rate)



packet = struct.pack("!cII", 'E'.encode(), socket.htonl(sequence), 0);
soc.sendto(packet, req_addr)

print("END PACKET")
print("send time:       ", datetime.now().isoformat(sep=" ", timespec="milliseconds"), sep="")
print("requester addr:  ", req_addr[0], ":", req_addr[1], sep="")
print("sequence:        ", sequence, sep="")
print("length:          ", 0, sep="")
print("payload:         ")
print()

f.close()
