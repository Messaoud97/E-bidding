import socket 
import threading
from tabulate import tabulate
from time import time

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

t = 0 
latest_bid = 0
conns = {}
item = {}
itemData = {}
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def send_items():
 f = open("biens.txt", "r")
 flines = f.readlines()
 for i in range(1, len(flines)):
    nline = flines[i].split()
 
    # Puts data in dictionary organized by {"Item Name":[Id,Price,....]} for updating and reading
    itemData[int(i)] = [(nline[0]), int(
        nline[1])]
 print(itemData)
       
 f.close()


def send_facture(addr) :
          f = open("facture.txt", "r")
          flines = f.readlines()
          for i in range(1 , len(flines)):
           nline = flines[i].split()
           print("here",nline[0],addr[1])
           if nline[0] == addr[1]:
            return("you have to pay : "+str(nline[1])).encode(FORMAT)
           
           return(('No facture for you !').encode(FORMAT))


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    if itemData == None : 
        print(f"[NO AUCTION]")
    else :
        listOfGlobals = globals()
        listOfGlobals['latest_bid'] = int(item[1])
        conn.send(str(item[1]).encode(FORMAT))
        t = time()+30
    connected = True
    while connected:
   
     if int(t) < int(time()) :
        f = open("hist.txt", "a")
        f.writelines(["\n"+str(addr[1])+"               "+str(latest_bid)+"          success"])
        f.close()
        f = open("facture.txt", "a")
        f.writelines(["\n"+str(addr[1])+"               "+str(float(latest_bid)*1.2)])
        f.close()
        for i in range(1, len(conns)+1) :
          conns[i].send(('[AUCTION CLOSED !]'+str(send_facture(addr))).encode(FORMAT))
 
     newbid= conn.recv(2048).decode(FORMAT)
     print(int(t),int(time()))
     if int(newbid) > int(latest_bid) and int(t) >int(time()) : 
        
        t=t+30 
        f = open("hist.txt", "a")
        f.writelines(["\n"+str(addr[1])+"               "+str(latest_bid)+"          echec"])
        f.close()
        listOfGlobals = globals()
        listOfGlobals['latest_bid'] = newbid

        for i in range(1, len(conns)+1) :
          if conns[i] != conn :
           conns[i].send(('[LOOSING] : '+str(newbid)).encode(FORMAT))
          else  :
           conns[i].send(('[WINNING !] : '+str(newbid)).encode(FORMAT))
     
  
        
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    send_items()
    for i in range(1, len(itemData)):    
     print(tabulate([itemData[i]], headers=['ID', 'PRICE']))

    selected = input("SELECT AN AUCTION ID : ") 
    global item
    item=(itemData[int(selected)])
    while True:

        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        conns[threading.activeCount() - 1]=conn


print("[STARTING] server is starting...")
start()