#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#client side
import socket
import threading

#creating the client side socket (cs)
cs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cs.connect(('127.0.0.1',49153 ))         
            #connect this client socket to out server's socket. also connect() is fucntion of socket module
    
    
#taking the nickname from the client
nickname = input("Enter the nickname: ")
#defining a recieve function to recieve anything from the server
def recieve():
    while True:
        try:
            message = cs.recv(1024).decode('ascii')    
            if message=='Nick':            # if the message is nick then we give the nickname to server 
                cs.send(nickname.encode('ascii')) 
            else:                          # if its not nick, then msg might be sth else so we just print it
                print(message)
        except:
            print("an error occurred :( ")   #if any error occurs while recieving the we jsut close the connection
            cs.close()
            break
            

# define a fucntion for writing and sending texts to server and hence to other clients as well
def write():
    while True:
        text = f'{nickname}:{input("")}' # take texts from the client
        cs.send(text.encode('ascii'))    # send it to the server
        
        
# now we create and start threads for recieve and write 
recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()


# In[ ]:


#server side 
import socket
import threading
import sys
import select

#deciding host IP address and port number for our server socket
host = '127.0.0.1'        # every localhost has this IP address
port =  49153         # of your choice just make sure its not used by any other. Their range is (0- 65535)


#creation of server socket
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         #socket function of socket module creates a socket object(ss here). And socket.AF_* , socket.SOCK_* constants define the type
         # of address taken and the type of socket created. here its INET and STREAM resptly.
ss.bind((host,port))
        # we bind our socket with the server IP and port number
ss.listen()
       # keep our server socket open for conncections. bind(), listen() belong to socket module 
    
    
# creating lists to store clients and their nicknames
clients = []
nicknames = []


#creating a broadcast function to broadcast msgs to connected clients
def broadcast(message):
    for client in clients:
        client.send(message)
               # send() is also in socket module 
            



#creating a handle function to handle client's messages when connected and send them to other clients
def handle(clientA):
    while True:       # starting an endless loop here
        try:
            message = clientA.recv(1024)
                      # recv() belongs to socket module and 1024 is the limit of bits of message clientA can give at a time. so
                      # so we recieve msg from 1 particular client. later we run this fnt on all indvidual clients
            broadcast(message)
                    # use our predifened broadcast function to spread the message of clientA to all other clients
        
        
        
         # if we recieve an error while recieving msg from clientA or broadcasting it we move to except 
                                      # step 1 : cut the connection of this clientA
                                      # step2 :remove him from the clients list  
                                      # step3 : terminate this function
        except:                                
            i = clients.index(clientA)   #index of clientA in clients list                         
            clients.remove(clientA)                                    
            close()                                               
                   #close() from socket module
                    #marks the end of socket
                    
            nickname = nicknames[i]  #nickname will be at same index in nicknames list as well
            broadcast(f'{nickname} left the chat'.encode(ascii))  #to send msg to tell other clients that clientA has been removed .
            nicknames.remove(nickname)  # remove him from nicknames list as well
            break
            

# function to recieve all the connections
def recieve():
    while True:
        client, address = ss.accept()  #if any connection is made by client, server will accept it and display that client 
        print(f'Connected with {str(address)}')                               # is connected on server side itself
        
        client.send('Nick'.encode('ascii'))     #if connected client will be asked for a nickname
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)                   # add the given nickname & client to our list of nicknames & clients
        clients.append(client)
        print(f'Nickname of the clients is {nickname}!')
        
        broadcast(f'{nickname} joined the chat!'.encode('ascii')) # tell all other clients that this client has joined
        client.send('connected to the server!'.encode('ascii'))      # tell our new client that he has connected
        
        
        thread = threading.Thread(target=handle, args=(client,)) # create a thread of process for every user which targets the handle 
        thread.start()                                           #function and argument is client
        
        
recieve()
       # ofc we need to call recieve method to recieve :)


# In[ ]:




