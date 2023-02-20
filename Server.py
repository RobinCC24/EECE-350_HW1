from socket import *
from time import *
import re

serverPort = 12000     #port picked at random      
serverSocket = socket(AF_INET, SOCK_STREAM) #creating socket
serverName = gethostname()  #getting the name of the host on which the code is being executed
serverSocket.bind((serverName, serverPort)) #binding the local host to the port
serverSocket.listen(1) #listening
print('Server started at', ctime())

while True:
    try:
        connectionSocket, addr = serverSocket.accept()  #accepting requests
        sentence = connectionSocket.recv(4096)  #saving the request
        sentence_str = sentence.decode()    #decoding the request from bytes to string        
        capitalizedSentence = sentence_str.upper()
        connectionSocket.send(capitalizedSentence.encode()) #sending the capitalized sentence to the connection socket
    
        match = re.search(r'Host:\s*(\S+)', sentence_str, re.IGNORECASE)    #serching in the request for what is after "Host:"
        if match:   #when found
            dest = match.group(1).encode()  
            destIP = gethostbyname(dest.decode())   #getting the requested IP
            destServer = socket(AF_INET, SOCK_STREAM)   #creating a socket for the destination server
            destServer.connect((destIP, 80))    #connecting the requested IP with port 80 for HTTP
            destServer.send(sentence)   #sending the request to the destination server
            print('The actual request was made at:', ctime())
            response = destServer.recv(4096).decode()   #receiving the response from the destination server
            print('The response was received at:', ctime())
            connectionSocket.send(response.encode())    #sending the response back to the client
            print('The response was sent back to the client at:', ctime())
    except error:
        print('ERROR!') #if there is an error from either the client or the server side
    destServer.close()  
    connectionSocket.close()    #closing the sockets
