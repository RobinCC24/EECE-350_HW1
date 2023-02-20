from socket import *
from time import *
import re, uuid

site = input('Enter the IP address of a website: ') #user input IP
serverPort = 12000  #port chosen randomly
serverName = gethostname()  #getting the name of the host on which the code is being executed

clientSocket = socket(AF_INET, SOCK_STREAM) #creating socket
clientSocket.connect((serverName, serverPort))  #connecting the host to the port

sentence = f"GET / HTTP/1.1\r\nHost: {site}\r\n\r\n"   #format of HTTP request
t0 = time() #saving the start time
print('The request', sentence, 'was sent to the server at:', ctime())

clientSocket.send(sentence.encode())    #sending the bytes to the client socket

#this part here was the only way for me to get the full html (source: https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data)
modifiedSentence = b''   #creating an empty byte string
while True:
    data = clientSocket.recv(4096)  #reading the html 4096 bytes at a time until it finds an empty string
    if not data:
        break
    modifiedSentence += data   #adding the bytes to the modifiedSentence (the reply)
    

print('The reply', modifiedSentence.decode(), 'is received back from the server at:', ctime())

t1 = time() #saving end time
RTT = t1 - t0   #total round-trip time
print('The total round-trip time is:', RTT)

clientSocket.close()    #closing the socket

print("My MAC address is:", ':'.join(re.findall('..', '%012x' % uuid.getnode())))   #printing MAC address

#source used for MAC address: https://www.geeksforgeeks.org/extracting-mac-address-using-python/
#source used for socket module functions: https://pythontic.com/modules/socket/introduction
#source used for time module: https://docs.python.org/3/library/time.html
