import argparse
import socket

soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

soc.bind((socket.gethostbyname(socket.gethostname()), 20000))

print(soc.recvfrom(8))

parser = argparse.ArgumentParser(prog='sender',description='sets up a file packet sender on specified port')

parser.add_argument('-p', '--port')          #port is the port on which the requester  waits for packets
parser.add_argument('-o', '--file_option')   #file_option is the name of the file that is being requested
args = parser.parse_args()











