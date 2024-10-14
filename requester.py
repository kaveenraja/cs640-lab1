import argparse
import socket
import struct

import time
from datetime import datetime

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


def proc_req(packet, host, port, filename, size):
    start_time = time.time_ns()
    next_sequence = -1
    total_bytes = 0
    total_packets = 0


    soc.sendto(packet, (host, port))

    f = open(filename, "a+")

    while 1:
        
        sen_packet, sen_addr = soc.recvfrom(9 + size)
        udp_header = struct.unpack("!cII", sen_packet[0:9])
        sequence = socket.ntohl(udp_header[1])

        if udp_header[0].decode() == 'E':
            print("END PACKET")
            print("recv time:       ", datetime.now().isoformat(sep=" ", timespec="milliseconds"), sep="")
            print("sender addr:     ", sen_addr[0], ":", sen_addr[1], sep="")
            print("sequence:        ", sequence, sep="")
            print("length:          ", 0, sep="")
            print("payload:         ", 0, sep="")
            print()
            break

        if next_sequence != -1 and next_sequence != sequence :
            print("ERROR: PACKET DROPPED")
            continue
        next_sequence = sequence + udp_header[2]

        f.write(sen_packet[9:udp_header[2] + 9].decode())
        total_bytes += udp_header[2];
        total_packets += 1

        print("DATA PACKET")
        print("recv time:       ", datetime.now().isoformat(sep=" ", timespec="milliseconds"), sep="")
        print("sender addr:     ", sen_addr[0], ":", sen_addr[1], sep="")
        print("sequence:        ", sequence, sep="")
        print("length:          ", udp_header[2], sep="")
        print("percentage:      ", round(total_bytes/size * 100, 2), "%"  ,sep="")
        print("payload:         ", sen_packet[9:13].decode(), sep="")
        print()



    f.close()

    end_time = time.time_ns()
    time_elasped = round((end_time - start_time) / 1000000)

    print("Summary")
    print("sender addr:             ", sen_addr[0], ":", sen_addr[1], sep="")
    print("Total Data packets:      ", total_packets, sep="")
    print("Total Data bytes:        ", total_bytes, sep="")
    print("Average packets/second:  ", round(total_packets/(time_elasped/1000)), sep="")
    print("Duration of the test:    ", time_elasped, "  ms" ,sep="")
    print()





for request in requests:
    udp_header = struct.pack("!cII", 'R'.encode(), 0, 0)
    r_packet = udp_header + request[0].encode()
    proc_req(r_packet, socket.gethostbyname(request[2]), int(request[3]), request[0], int(request[4].removesuffix("B\n")))

    













