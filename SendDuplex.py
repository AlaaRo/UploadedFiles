#!/usr/bin/python3
import threading
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
import socket
import os

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
IP = input("Server IP address or Hostname: ")
s.connect((IP,4567))
print(f"Socket1 connected to {IP}")


def graphical():
    Tk().withdraw()
    filenames = askopenfilenames()
    return list(filenames)   

"""def textual():
    filenames = []
    while True:
        filename = input("File name or path to send. Submit an empty name to start sending: ")
        if filename == '':
            break
        if os.path.exists(filename.strip()) == True and os.path.isfile(filename.strip()) == True:
            filenames.append(filename.strip())
            print(f"File names supplied: {' '.join(filenames)}")
        else:
            print(f"'{filename}' doesn't exist or it's not a file")
            print(f"File names supplied: {' '.join(filenames)}")
    return filenames"""

def sender():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    totalsent = []
    while True:
        filenames = graphical()
        if not filenames:
            break
        name_size_list = []
        for filename in filenames:
            size = str(os.path.getsize(filename))
            name_size_list.append(os.path.basename(filename))
            name_size_list.append(size)
        print(name_size_list)
        name_size = "|".join(name_size_list)
        s.send(name_size.encode())
        for filename in filenames:
            if s.recv(2).decode() == "GO":
                with open(filename,"rb") as f:
                    filecontents = f.read()
                    s.sendall(filecontents)
                    totalsent.append(filename)
    print(f"total files sent: {len(totalsent)}")
    return f"total files sent: {len(totalsent)}"

            
def reciever():
    s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s2.connect((IP,4567)
    print(f"Socket2 connected to {IP}")
    totalrecved = []
    try:
        os.mkdir("RecievedFiles")
    except FileExistsError:
        pass
    while True: 
        names_sizes = s2.recv(2048).decode()
        if not names_sizes:
            break
        print(f"DECODED STRING : '{names_sizes}'")
        name_size_list = names_sizes.split("|")
        print("LIST:",name_size_list)
        for i in range(0,len(name_size_list)-1,2):
            s2.send("GO".encode())                
            with open(f"RecievedFiles/{name_size_list[i]}","wb") as f:
                f.write(s2.recv(int(name_size_list[i+1])))
                totalrecved.append(name_size_list[i])
    print(f"total files recieved: {len(totalrecved)}")
    return f"total files recieved: {len(totalrecved)}"

Trecv = threading.Thread(target=reciever)
Tsend = threading.Thread(target=sender)
Trecv.start()
print("READY TO RECIEVE....")
Tsend.start()
    
    
