# Secured-File-Transfer

Problem Description:
Suppose there are 'n' users A (clients) want to securely access the files stored in the database of a user B (server).
At first, each client will make a connection using socket with the server B and then will establish three symmetric keys, say K 1 , K 2 and K 3 which will be used for encryption and decryption using the 3DES with three keys symmetric cryptosystem.

Part_1-
For establishment of a shared session key K A,B between the client A and the server B, the Diffie-Hellman key exchange protocol is used.

Part_2-
Assume that each client A has already established three symmetric keys K 1 , K 2 and K 3 using Part_1. Now the communication initiates securely using the 3DES algorithm of data transfer.

It follows a particular header data structure for transimission:

• A client (A) sends a request message REQSERV for requesting the service (transferring a requested file) from the server (B).
• Suppose the server (B) is allowed to transmit at a time a maximum of 1024 bytes to a client (A). After receiving the message REQERV, if the requested file is not present at the server (B), an appropriate message (DISCONNECT) will be sent by the server B to the client (A) indicating the ‘no such file exists’. Otherwise, the server (B) will send the encrypted messages ENCMSG on the file to the client (A) at a time a maximum of 1024 bytes until the entire file is transferred.
• Finally, a completion message REQCOM will be sent from the server (B) to the client (A) to indicate that the whole file has been successfully transmitted followed by DISCONNECT messages.
