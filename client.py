SERVER_IP = '0.0.0.0'
SERVER_PORT = 12345
from socket import *
import sys
sock = socket()
sock.connect((SERVER_IP,SERVER_PORT))
print('Connection established')
in_stream = sock.makefile('r')
sock.send('CONNECTION,\r\n')
response = in_stream.readline().strip()
hashtype = '0'
while response != "":
    data = response.split('|')
    state = data[0]
    msg = data[1].replace(',','\n')
    if state == 'MENU':
        option = raw_input(msg + '-> ')
        hashtype = option
        sock.send(option+',\r\n')
    elif state == 'ENTER_TEXT':
        option = raw_input(msg + '-> ')
        sock.send(hashtype+','+option+'\r\n')
    elif state == 'ENCRYPTED':
        print(msg)
        break
    response = in_stream.readline().strip()
in_stream.close()
sock.close()
