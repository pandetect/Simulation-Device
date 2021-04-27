import argparse 
import socket
import time

def create_invoker():
    return str.encode('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Device simulator')
    parser.add_argument('--addr', type=str, default='127.0.0.1') # address
    parser.add_argument('--p', type=int, default=3333) # port

    # parse arguments
    args = parser.parse_args()

    print('Trying to connect to the server')

    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((args.addr, args.p))
                print('Connected to:', args.addr)

                while True: # get packages forever
                    invoker = create_invoker()

                    s.sendall(invoker)

                    print('Sent invocation waiting for package', end='')

                    package_header = s.recv(12)

                    if not package_header: 
                        print('\nClosed connection')
                        break

                    package_header_index  = int.from_bytes(package_header[0:8], byteorder='big')
                    package_header_length = int.from_bytes(package_header[8:12], byteorder='big')

                    print('Index:', package_header_index, 'Length:', package_header_length, end='')

                    package_data_body = b''
                    package_data_remain = package_header_length + 1

                    while True:
                        print('-', end='', sep='')
                        package_data_temp = s.recv(package_data_remain)

                        if not package_data_temp: 
                            print('\nClosed connection!')
                            break

                        package_data_body += package_data_temp
                        package_data_remain -= len(package_data_temp)

                        if package_data_remain == 0:
                            break
                        
                    print(' Recieved', len(package_data_body) - 1, 'bytes')

                    time.sleep(0.250) # sleep 250 ms
        except ConnectionRefusedError as e:
            time.sleep(0.100) # sleep for 100 ms
            