

import socket
import struct


class Message:

    def __init__(self, seq_nr, msg):
        self.seq = seq_nr
        self.msg = msg 


    def as_bytes(self):

        msg_bytez = self.msg.encode('utf-8')
        msg_len = len(msg_bytez)

        bytez_header = struct.pack('ii',self.seq,msg_len)
        bytez = bytearray(bytez_header)
        bytez.extend(bytearray(msg_bytez))
    
        return bytez

    def __str__(self):
        return f"[{self.seq}]: {self.msg}"

    def __repr__(self) -> str:
        return self.__str__()


def send_msg(stream,msg:Message):
    stream.sendall(msg.as_bytes())

def recv_msg(stream)->Message:

    header = stream.recv(8)
    seq,len = struct.unpack('ii',header)

    msg = stream.recv(len)
    msg = msg.decode('utf-8')

    return Message(seq,msg)





def main():
    HOST = "127.0.0.1"  # The server's hostname or IP address
    #HOST="https://tuct2k22-4v43eh3xsa-lz.a.run.app/"
    PORT = 1337  # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        
        m1 = Message(1,"1")
        send_msg(s,m1)

        m2 = recv_msg(s)
        if m2.seq == 2:
            print("Tree connection initiated!")
        else:
            print("Failed to connect ot treee master")
            raise Exception("oof")


        while True:

            msg = recv_msg(s)
            print(msg)

            if msg.seq == 10:
                resp = Message(11,"glass e gött")
                send_msg(s,resp)
            else:
                break



if __name__ == '__main__':
    main()



