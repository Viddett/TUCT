import pico_tcp_dummy as p 
import socket

import json



def main():
    HOST = "127.0.0.1"  # The server's hostname or IP address
    #HOST="https://tuct2k22-4v43eh3xsa-lz.a.run.app/"
    PORT = 1337  # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        req = {"tree_id":1,"msg":"gillareu_glass?"}

        js_strin = json.dumps(req)

        m1 = p.Message(30,js_strin)
        
        p.send_msg(s,m1)

        m2 = p.recv_msg(s)

        print(m2)




if __name__ == '__main__':
    main()

