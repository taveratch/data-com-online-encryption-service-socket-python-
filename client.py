# -- members
#   1. TAWEERAT CHAIMAN 5710546259
#   2. PATINYA YONGYAI 5710547204
# *** Supported python 3.5.x

from socket import *
import sys
# -- constants
SERVER_IP = '0.0.0.0'
SERVER_PORT = 12345
hashtype = '0'

# -- define socket and make a connection
sock = socket()
sock.connect((SERVER_IP,SERVER_PORT))
print('Connection established')
in_stream = sock.makefile('r')

# -- send command to get menu from server
sock.send('CONNECTION,\r\n'.encode())
# -- read first msg from server
response = in_stream.readline().strip()

# magic happens here
while response != "":
    # -- split the data according on our protocol
    #    Protocol -> ['STATE','MSG']
    data = response.split('|')
    state = data[0]
    msg = data[1].replace(',','\n')

    # -- states
    if state == 'MENU':
        option = input(msg + '-> ')
        hashtype = option
        sock.send((option+',\r\n').encode())
    elif state == 'ENTER_TEXT':
        option = input(msg + '-> ')
        sock.send((hashtype+','+option+'\r\n').encode())
    elif state == 'ENCRYPTED':
        print(msg)
        break
    elif state == 'ERROR':
        print(msg)
        break
    response = in_stream.readline().strip()

# -- close the connection and socket
in_stream.close()
sock.close()
