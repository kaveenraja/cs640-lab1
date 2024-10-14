import argparse
import socket
import struct
import time

#Args
parser = argparse.ArgumentParser(prog='sender',description='sets up a file packet sender on specified port')

parser.add_argument('-p', '--port')          #port is the port on which the requester  waits for packets
parser.add_argument('-o', '--file_option')   #file_option is the name of the file that is being requested
args = parser.parse_args()


# Socket set up
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.bind((socket.gethostbyname(socket.gethostname()), int(args.port)))


#Open file
requests = []
file = open("tracker.txt", "r")

for line in file:
    if args.file_option in line:
        requests.append(line.split(" "))

requests.sort(key=lambda x: x[1])


def proc_req(packet, host, port, size):
    soc.sendto(packet, (host, port))

    while 1:
        
        sen_packet, sen_addr = soc.recvfrom(9 + size)

        break



for request in requests:
    udp_header = struct.pack("!cII", 'R'.encode(), 0, 0)
    r_packet = udp_header + request[0].encode()
    proc_req(r_packet, socket.gethostbyname(request[2]), int(request[3]), int(request[4]))

    













