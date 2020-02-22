import socket
import sys
from threading import Thread 
import pyDH
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

c = pyDH.DiffieHellman()
pubkey = c.gen_public_key()
shared_secret= ""

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((sys.argv[1], int(sys.argv[2])))


hdr= Header("10", "127.0.0.1", "127.0.0.1")
msg= Message(hdr)
msg.PubKey= str(pubkey)
data_packet= pickle.dumps(msg)
client.send(str(len(data_packet)).encode('utf8'))
client.send(data_packet)

length= int(client.recv(3).decode('utf8'))
temp= client.recv(length)
received= pickle.loads(temp)
value= int(received.PubKey)
shared_secret= c.gen_shared_key(value)
shared_secret= shared_secret[:24]


print("Enter the filename you want to access.")
filename= input()

hdr= Header("20", "127.0.0.1", "127.0.0.1")
msg= Message(hdr)
msg.ReqServ= filename
data_packet= pickle.dumps(msg)
client.send(str(len(data_packet)).encode('utf-8'))
client.send(data_packet)

length= int(client.recv(3).decode('utf-8'))
temp= client.recv(length)
received= pickle.loads(temp)

if(received.header.opcode =='50'):
	print("Oops! The requested file does not exist. Try Again....")

elif(received.header.opcode == '30'):
	k= pyDes.triple_des(shared_secret.encode('utf-8'), pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
	with open(filename, 'wb') as file:
		while(received.header.opcode == '30'):
			buffer= k.decrypt(received.EncMsg)
			file.write(buffer)

			length= int(client.recv(3).decode('utf-8'))
			temp= client.recv(length)
			received= pickle.loads(temp)
			
	file.close()
	if(received.header.opcode == '40'):
		print ("File received succesfully.")
	else:
		print ("File reception failed.")

	
	hdr= Header("50", "127.0.0.1", "127.0.0.1")
	msg= Message(hdr)
	msg.Disconnect= 'DISCONNECT'
	data_packet= pickle.dumps(msg)
	client.send(str(len(data_packet)).encode('utf-8'))
	client.send(data_packet)
	length= int(client.recv(3).decode('utf8'))
	received= client.recv(length)
	client.close()
