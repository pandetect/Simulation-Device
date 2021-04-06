# This program takes the ip and the port from the commandline arguments.
# then runs the webcam

import argparse 
import socket

def create_package(packet_index, dummy=True):
    if dummy:
        data = str.encode('A' * 650000)
    else:
        raise NotImplementedError()

    header_1 = packet_index.to_bytes(8, byteorder='big')
    header_2 = len(data).to_bytes(4, byteorder='big')
    tail     = str.encode('\n')

    return header_1 + header_2 + data + tail


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Device simulator')
    parser.add_argument('--p', type=int, default=3344) # port

    # parse arguments
    args = parser.parse_args()

   

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.01', args.p))
        s.listen()

        while True:
            print('Ready to accept connections')
            
            conn, addr = s.accept()

            with conn:
                packet_index = 0
                print('Sending data to', addr)

                while True:
                    data = conn.recv(1) # get the new line operator

                    if not data: 
                        print('Connection closed')
                        break
                    
                    package = create_package(packet_index, dummy=True)
                    conn.sendall(package)

                    print('Sent package:', packet_index)
                    packet_index += 1


        print('Connection lost exitting...')
