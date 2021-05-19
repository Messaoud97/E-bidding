import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.3"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send():

    print(f"[------------AVAILABLE AUCTION----------------]")
    print(f"[AUCTION STARTING PRICE : ]",client.recv(2048).decode(FORMAT),"$")


    connected = True
    while connected:
     
       aux = input("BIDDING AGAIN ? y/n : ")
       if  aux != 'n' :
        bid = input("ENTER THE AMOUNT : ")
        client.send(bid.encode(FORMAT))
         
        print(client.recv(2048).decode(FORMAT))
       
       else :
        print(client.recv(2048).decode(FORMAT))
         
       

          

    send(DISCONNECT_MESSAGE)
 
 

send()