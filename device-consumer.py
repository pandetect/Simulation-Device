import argparse 
import socket
import time
import threading
import cv2
import numpy as np
import io
from PIL import Image
import sys
import fileinput
import select

def create_invoker():
    return str.encode('\n')

__close_requested = False

def thread_communication(conn, addr, show_images=False):
    global __close_requested
    with conn:

        while not __close_requested:

            invoker = create_invoker()

            # print('Sending', invoker)
            conn.sendall(invoker)

            package_header = conn.recv(12)

            if not package_header:
                cv2.destroyAllWindows()
                print('\nClosed connection')
                break

            package_header_index  = int.from_bytes(package_header[0:8], byteorder='little')
            package_header_length = int.from_bytes(package_header[8:12], byteorder='little')

            # print('From', addr, 'Index:', package_header_index, 'Length:', package_header_length, end=' ')

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
            
            # print(' [chunks=', num_chunks, '] ', end='', sep='')
            # print(' Recieved', len(package_data_body), 'bytes')

            if show_images:
                # buffer_bytes_array = bytearray(package_data_body[:-1])
                # bytes_io = io.BytesIO(package_data_body)
                # pil_image = Image.open(bytes_io)
                # frame = np.asarray(pil_image)
                # frame = np.resize(frame, (100, 100, 3))

                # frame = np.fromstring(package_data_body.decode('ascii'), dtype=np.int8, sep=' ')
                #frame = np.frombuffer(package_data_body, dtype=np.int)

                #frame = np.resize(frame, (500, 500, 3))
                reversed_data_body = b''
                for b in package_data_body:
                    reversed_data_body += b.to_bytes(1, byteorder='little')

                image = Image.open(io.BytesIO(bytearray(reversed_data_body)))
                frame = np.array(image)
                frame = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)

                # a = np.array([1, 2, 3])

                # print(frame)
                cv2.imshow('Frame', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break

                # print(package_data_body.decode('ascii'))

def GetChar(Block=True):
  if Block or select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
    return sys.stdin.read(1)
  return ''

def thread_userinput():
    global __close_requested
    while True:
        # print('muzo')
        # req = input()
        # print('muzo der ki', req)
        try:
            req = GetChar(False)
        except Exception:
            return 

        if not 'q' in req: continue

        __close_requested = True

        break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Device simulator')
    parser.add_argument('--p', type=int, default=3333) # port

    thread_vector = []

    # parse arguments
    args = parser.parse_args()
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    print('Accepting connections', ip_address, hostname)

    user_t = threading.Thread(target=thread_userinput)
    user_t.start()


    while not __close_requested:

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('192.168.1.34', args.p))
                s.listen()
            except Exception as e :
                print(e)
                __close_requested = True
                exit(-1)


            while not __close_requested:
                conn, addr = s.accept()


                print('Connected to:', addr[0])

                t = threading.Thread(target=thread_communication, args=(conn, addr))
                t.start()
                thread_vector.append(t)
    

                
