




import socket
import struct

HOST = "127.0.0.1"  # The server's hostname or IP address
#HOST="https://tuct2k22-4v43eh3xsa-lz.a.run.app/"
PORT = 1337  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    
    txt = [str(i+1) for i in range(37)]
    txt = ''.join(txt)
    txt = '1337'

    txt_bytez = txt.encode('utf-8')
    print(txt_bytez)
    print(len(txt_bytez))

    bytez = struct.pack('ii',1,len(txt_bytez))
    s.sendall(bytez)
    s.sendall(txt_bytez)

    data = s.recv(8)
    print(data)






