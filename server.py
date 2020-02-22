import socket
import sys
import threading
from threading import Thread 
import pyDH
from os import path
import os
import pyDes
import time
import pickle

class Header:
    def __init__(self, opcode, sender, destination):
        self.opcode= opcode
        self.sender= sender
        self.destination= destination

class Message:
    def __init__(self, header):
        self.header= header

    PubKey= str()
    ReqServ= str()
    ReqCom= str()
    EncMsg= str()
    Disconnect= str()

s = pyDH.DiffieHellman()
pubkey = s.gen_public_key()
shared_secret=""



def ClientThread(conn, addr): 
 
    while True:
        length= int(conn.recv(3).decode('utf8'))
        temp= conn.recv(length)          
        received= pickle.loads(temp)

        if received.header.opcode== '10':

            global shared_secret
            value= int(received.PubKey)
            shared_secret= s.gen_shared_key(value)
            shared_secret= shared_secret[:24]

            hdr= Header("10", "127.0.0.1", "127.0.0.1")
            msg= Message(hdr)
            msg.PubKey= str(pubkey)
            data_packet= pickle.dumps(msg)
            conn.send(str(len(data_packet)).encode('utf-8'))
            conn.send(data_packet)

        if received.header.opcode == '20':
            if path.exists(received.ReqServ) == False:
                hdr= Header("50", "127.0.0.1", "127.0.0.1")
                msg= Message(hdr)
                msg.Disconnect= 'DISCONNECT'
                data_packet= pickle.dumps(msg)
                conn.send(str(len(data_packet)).encode('utf-8'))
                conn.send(data_packet)

            else:
                k= pyDes.triple_des(shared_secret.encode('utf-8'), pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
                with open(received.ReqServ, 'rb') as file:
                    
                    while(True):
                        buffer= file.read(512)
                        if(len(buffer) ==0):
                            hdr= Header("40", "127.0.0.1", "127.0.0.1")
                            msg= Message(hdr)
                            msg.ReqCom= 'REQCOM'
                            data_packet= pickle.dumps(msg)
                            conn.send(str(len(data_packet)).encode('utf-8'))
                            conn.send(data_packet)
                            print ("File transmitted succesfully")
                            break

                        hdr= Header("30", "127.0.0.1", "127.0.0.1")
                        msg= Message(hdr)
                        msg.EncMsg= k.encrypt(buffer)
                        data_packet= pickle.dumps(msg)
                        conn.send(str(len(data_packet)).encode('utf-8'))
                        conn.send(data_packet)

                file.close()
                
                length= int(conn.recv(3).decode('utf8'))
                received= conn.recv(length)
                hdr= Header("50", "127.0.0.1", "127.0.0.1")
                msg= Message(hdr)
                msg.Disconnect= 'DISCONNECT'
                data_packet= pickle.dumps(msg)
                conn.send(str(len(data_packet)).encode('utf-8'))
                conn.send(data_packet)
                
                return



serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((sys.argv[1], int(sys.argv[2]))) #ip:port
serv.listen(5)
while True:
    conn, addr = serv.accept()
    newThread= threading.Thread(target= ClientThread, args= (conn, addr))
    newThread.start()

conn.close()

