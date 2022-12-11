
import _thread,time,network
import wifi_creds

try:
    import usocket as socket
except:
    import socket



def connect_wifi(timeout_s:int=9):

    wlan = network.WLAN(network.STA_IF) #initialize the wlan object
    wlan.active(True)

    wlan.config(pm = 0xa11140)

    wlan.connect(wifi_creds.wifi_ssid, wifi_creds.wifi_pswd)


    wait_time = 0
    while not wlan.isconnected() and wlan.status() >= 0:
        print("Waiting to connect...")
        time.sleep(1)
        wait_time += 1

        if wait_time > timeout_s:
            raise Exception("Failed to connect to wifi!")

    print(wlan.ifconfig())


class HttpServer:

    def __init__(self, get_callback, post_callback):
        self._get_callback = get_callback
        self._post_callback = post_callback
        self._stop_flag = False


    def start_server(self,backlog:int=5,port:int=80):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(1.5)
        self.socket.bind(('', port))
        self.socket.listen(backlog)
        self.stop_webserver = False
        _thread.start_new_thread(self._server_thread,())

    def _server_thread(self):
        while not self._stop_flag:

            #conn, addr = self.socket.accept()
            #"""
            try:
                print("wait accept new conn")
                conn, addr = self.socket.accept()
            except OSError as e:
                if e.errno == 110:
                    continue
                else:
                    raise e
            #"""
            print('Got a connection from %s' % str(addr))
            self._handle_conn(conn,addr)

        self.socket.close()
        print("Server stopped")

    def stop_server(self):
        self._stop_flag = True 
        while self._stop_flag:
            time.sleep_ms(200)


    def _handle_conn(self,conn, addr):
        request = conn.recv(2024)
        #request2 = conn.recv(1024)
        request = request.decode("utf-8") 
        
        self._send_response_http(conn)
        conn.close()

        request_lines = request.split('\n')

        method = request_lines[0].split('/')[0].replace(' ','')
        args = dict()

        for line in request_lines[1:]:
            line = line.strip()
            if ':' in line:
                parts = line.split(':')

                args[parts[0]] = parts[1]
        print(method)
        print(args)




    def _send_response_http(self,conn,args=dict()):

        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n')
        for arg in args:
            conn.sendall(arg + ':' + str(args[arg]) + '\n')
        conn.sendall('\n')


def get_callback(args):
    print("GET CALLBACK")

def post_callback(args):
    print("POST CALLBACK")



if __name__ == '__main__':

    print("connecting to wifi")
    connect_wifi()
    print("starting server")
    server = HttpServer(get_callback,post_callback)
    server.start_server()

    #while True:
    #    time.sleep_ms(200)
    print("eeee")
    time.sleep(35)
    print("bytbey")
    server.stop_server()

    time.sleep(2)

