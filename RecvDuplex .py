#!/usr/bin/python3
import socket
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
import os
import threading
#import subprocess
#CP = subprocess.run(["hostname","-I"],capture_output=True)
#IP = CP.stdout.decode().strip()
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(("",4567))
s.listen(0)
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

def reciever():
        totalrecved = []
        ct1,address1 = s.accept()
        print(f"Socket1 CONNECTED: {address1}")
        try:
                os.mkdir("RecievedFiles")
        except FileExistsError:
                pass
        while True: 
                names_sizes = ct1.recv(2048).decode()
                if not names_sizes:
                        break
                print(f"DECODED STRING : '{names_sizes}'")
                name_size_list = names_sizes.split("|")
                print("LIST:",name_size_list)
                for i in range(0,len(name_size_list)-1,2): 
                        ct1.send("GO".encode())                
                        with open(f"RecievedFiles/{name_size_list[i]}","wb") as f:
                                f.write(ct1.recv(int(name_size_list[i+1])))
                                totalrecved.append(name_size_list[i])
        print(f"total files recieved: {len(totalrecved)}")
        return f"total files recieved: {len(totalrecved)}"

def sender():
        totalsent = []
        ct2,address2 = s.accept()
        print(f"Socket2 CONNECTED: {address2}")
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
                ct2.send(name_size.encode())
                for filename in filenames:
                    if ct2.recv(2).decode() == "GO":
                        with open(filename,"rb") as f:
                            filecontents = f.read()
                            ct2.sendall(filecontents)
                            totalsent.append(filename)
        print(f"total files sent: {len(totalsent)}")
        return f"total files sent: {len(totalsent)}"

Trecv = threading.Thread(target=reciever)
Tsend = threading.Thread(target=sender)
Trecv.start()
print("READY TO RECIEVE....")
Tsend.start()
