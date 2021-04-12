# This program takes the ip and the port from the commandline arguments.
# then runs the webcam

import argparse 
import socket
import time

def create_package(packet_index, dummy=True):
    if dummy:
        data = str.encode('A' * 10)
    else:
        raise NotImplementedError()

    header_1 = packet_index.to_bytes(8, byteorder='big')
    header_2 = len(data).to_bytes(4, byteorder='big')
    tail     = str.encode('\n')

    return header_1 + header_2 + data + tail


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Device simulator')
    parser.add_argument('--addr', type=str, default='localhost') # address
    parser.add_argument('--p', type=int, default=3338) # port

    # parse arguments
    args = parser.parse_args()

    print('Ready to accept connections')
   
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((args.addr, args.p))

                packet_index = 0

                while True:
                    data = s.recv(1) # get the new line operator

                    if not data: 
                        print('Connection closed')
                        break
                    
                    package = create_package(packet_index, dummy=True)
                    s.sendall(package)

                    print('Sent package:', packet_index)
                    packet_index += 1

                print('Connection lost exitting...')
                
        except ConnectionRefusedError as e:
            time.sleep(0.100) # sleep 100 ms
