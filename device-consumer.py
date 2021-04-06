import argparse 
import socket
import time
import threading
import cv2
import numpy as np
import io
from PIL import Image

def create_invoker():
    return str.encode('\n')

def thread_communication(conn, addr, show_images=True):
    with conn:
        while True:
            invoker = create_invoker()

            conn.sendall(invoker)

            package_header = conn.recv(12)

            if not package_header:
                cv2.destroyAllWindows()
                print('\nClosed connection')
                break

            package_header_index  = int.from_bytes(package_header[0:8], byteorder='big')
            package_header_length = int.from_bytes(package_header[8:12], byteorder='big')

            print('Index:', package_header_index, 'Length:', package_header_length, end=' ')

            package_data_body = b''
            package_data_remain = package_header_length
            num_chunks = 0

            while True:
                num_chunks += 1
                package_data_temp = conn.recv(package_data_remain)

                if not package_data_temp: 
                    print('\nClosed connection!')
                    break

                package_data_body += package_data_temp
                package_data_remain -= len(package_data_temp)

                if package_data_remain == 0:
                    break

            if not package_data_temp:
                cv2.destroyAllWindows()
                break
            
            print(' [chunks=', num_chunks, '] ', end='', sep='')
            print(' Recieved', len(package_data_body), 'bytes')

            if show_images:
                # buffer_bytes_array = bytearray(package_data_body[:-1])
                # bytes_io = io.BytesIO(package_data_body)
                # pil_image = Image.open(bytes_io)
                # frame = np.asarray(pil_image)
                # frame = np.resize(frame, (100, 100, 3))

                # frame = np.fromstring(package_data_body.decode('ascii'), dtype=np.int8, sep=' ')
                frame = np.frombuffer(package_data_body, dtype=np.int)

                frame = np.resize(frame, (100, 100, 3))

                # a = np.array([1, 2, 3])

                

                print(frame)
                cv2.imshow('Frame', frame)

                

                # print(package_data_body.decode('ascii'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Device simulator')
    parser.add_argument('--p', type=int, default=3338) # port

    thread_vector = []

    # parse arguments
    args = parser.parse_args()
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    print('Accepting connections', ip_address, hostname)


    while True:
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('192.168.1.34', args.p))
            s.listen()

            while True:
                conn, addr = s.accept()

                print('Connected to:', addr)

                t = threading.Thread(target=thread_communication, args=(conn, addr))
                t.start()
                thread_vector.append(t)


                
