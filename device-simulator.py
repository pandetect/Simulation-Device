# This program takes the ip and the port from the commandline arguments.
# then runs the webcam


# TO RUN
# python .\device-simulator.py --addr 192.168.1.36 --p 3333

import argparse 
import socket
import time
import cv2
from PIL import Image
import numpy as np
import io

def create_package(capture, packet_index, dummy=False, show_window=True):
    if dummy:
        data = str.encode('abcdefg')
    else:
        ret, frame = capture.read()

        # success, a_np = cv2.imencode('.jpg', frame)


        frame = cv2.resize(frame, (500, 500))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        pil_image = Image.fromarray(frame)
        byte_io = io.BytesIO()
        pil_image.save(byte_io, format='JPEG')
        data = byte_io.getvalue()

        # data = frame.astype('int').tobytes()

        data_new = b''

        for b in data:
            data_new += int(b).to_bytes(1, 'little')

        # print(type(data))

        # data = frame.tobytes()

        if show_window:
            cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            return None

    header_1 = packet_index.to_bytes(8, byteorder='little')
    header_2 = len(data_new).to_bytes(4, byteorder='little')
    tail     = str.encode('\n')

    return header_1 + header_2 + data_new


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Device simulator')
    parser.add_argument('--addr', type=str, default='localhost') # address
    parser.add_argument('--p', type=int, default=3333) # port

    capture = cv2.VideoCapture(0)

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
                    
                    package = create_package(capture, packet_index)

                    if not package:
                        print('Exitting')
                        raise KeyError('exit requested')

                    s.send(package)

                    print('Sent package:', packet_index)
                    packet_index += 1

                    time.sleep(0.1)

                print('Connection lost exitting...')
                
        except ConnectionRefusedError as e:
            time.sleep(0.100) # sleep 100 ms
        except KeyError as k:
            break
