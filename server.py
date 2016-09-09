import sys
from socket import *
import hashlib
import base64
import time

# -- constants
SERVER_PORT = 12345
types = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512'] # type of encryption

# -- methods
def make_connection():
    global sock,info,addr,port,in_stream,listen_sock
    sock,info = listen_sock.accept() # accept client's connection
    addr,port = sock.getpeername() # get client's ip and port
    sys.stdout.flush()  # make the above output show up immediately
    in_stream = sock.makefile('r') # create steam
    log("Client is connected from " + addr + " port : " + str(port))

def hash_text(hashtype,text): # use hashlib to hash the text
    if hashtype == '1':
        return hashlib.md5(text).hexdigest()
    elif hashtype == '2':
        return hashlib.sha1(text).hexdigest()
    elif hashtype == '3':
        return hashlib.sha224(text).hexdigest()
    elif hashtype == '4':
        return hashlib.sha256(text).hexdigest()
    elif hashtype == '5':
        return hashlib.sha384(text).hexdigest()
    elif hashtype == '6':
        return hashlib.sha512(text).hexdigest()
    else: # default is md5
        return hashlib.md5(text).hexdigest()

def log(text): # print log on server side
    print(text)
    print("log : timestamp : " + str(time.time()))

# -- listening for clients
listen_sock = socket() # create instance of socket
listen_sock.bind(('0.0.0.0',SERVER_PORT)) # bind ip and port to server
listen_sock.listen(10) # listening with limited number of connection
log("Listening on port " + str(SERVER_PORT))
make_connection()

# -- magic happens here
while True: # listening
    msg = in_stream.readline().strip() # receive message from client
    if msg == '':
        make_connection()
        continue
    msgs = msg.split(',')
    if msgs[0] == 'CONNECTION': #send to menu to client
        sock.send('MENU|')
        sock.send('Please choose type of hash,')
        sock.send('1. md5,')
        sock.send('2. sha1,')
        sock.send('3. sha224,')
        sock.send('4. sha256,')
        sock.send('5. sha384,')
        sock.send('6. sha512,\r\n')
    elif msgs[0] in '123456' and msgs[1] == '': # wait for plain text
        hashtype = types[int(msgs[0])-1]
        log("log : using " + hashtype)
        sock.send('ENTER_TEXT|')
        sock.send('Please enter plain text to encrypt ('+hashtype+') : \r\n')
    elif len(msgs) >= 2 and len(msgs[1]) > 0: # send encrypted text to client
        log('log : returned encrypted text')
        sock.send('ENCRYPTED|')
        sock.send('Encrypted text ('+ types[int(msgs[0])-1]+') : ')
        sock.send(str(hash_text(msgs[0],msgs[1]))+',\r\n'.encode())
        make_connection() # make new connection
    else: # throw an error
        sock.send('ERROR|')
        sock.send('Error terminating program\r\n')

# -- close the connection and socket.
print("Client closed connection")
in_stream.close()
sock.close()
listen_sock.close()
print ('Server stopped listening')
