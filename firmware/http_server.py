
import time,network
import wifi_creds
import json
import index

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

    def __init__(self, get_state_callback, post_callback):
        self._get_callback = get_state_callback
        self._post_callback = post_callback
        self._stop_flag = False

        self._html_response = index.html


    def start_server(self,backlog:int=5,port:int=80):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(1.5)
        self.socket.bind(('', port))
        self.socket.listen(backlog)
        self.stop_webserver = False
        #_thread.start_new_thread(self._server_thread,())

    def _server_thread(self):
        while not self._stop_flag:

            try:
                # self.socket.settimeout(1.5) determines the timeout here
                conn, addr = self.socket.accept()
            except OSError as e:
                if e.errno == 110:
                    continue
                else:
                    raise e

            print('Got a connection from %s' % str(addr))
            self._handle_conn(conn,addr)

        self.socket.close()
        print("Server stopped")




    def stop_server(self):
        self._stop_flag = True 
        while self._stop_flag:
            time.sleep_ms(200)


    def _handle_conn(self,conn, addr):
        request = ""
        req_bytes = conn.recv(1024)
        request = req_bytes.decode("utf-8") 
        #print(request)
        
        request_lines = request.split('\n')

        method = request_lines[0].split(' ')[0]
        url = request_lines[0].split(' ')[1].strip()
        args = dict()

        for line in request_lines[1:]:
            line = line.strip()
            if ':' in line:
                parts = line.split(':')
                args[parts[0]] = parts[1]

        if method == 'OPTIONS':
            self._send_cors_stuff(conn)
            
        elif method == 'GET':
            self._send_cors_stuff(conn)
            self._handle_get(conn,url,args,request)

        elif method == 'POST':

            self._send_cors_stuff(conn)
            self._handle_post(conn,url,args,request)

        else:

            self._send_bad_req(conn)

        conn.close()
        print("Closed")

    def _send_bad_req(self,conn):
            conn.send('HTTP/1.1 400 Bad request\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n')
            conn.sendall('\n')

    def _send_cors_stuff(self,conn):
        resp_stuff = [
            "Access-Control-Allow-Origin: *",
            "Access-Control-Allow-Credentials : true",
            "Access-Control-Allow-Methods : GET,HEAD,OPTIONS,POST,PUT",
            "Access-Control-Allow-Headers:Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
            ]

        conn.send('HTTP/1.1 200 OK\n')

        for r in resp_stuff:
            conn.sendall(r + '\n')


    def _handle_get(self,conn,url,args,request):

        if url == '/':
            # Default landing page
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.send(self._html_response)
            
        elif url == '/state':
            # return tree state as json
            #print("get state")
            state = self._get_callback()
            state_json = json.dumps(state)
            conn.send('Content-Type: application/json\n\n')
            conn.send(state_json + '\n')
        else:
            # Bad request
            self._send_bad_req(conn)

    def _handle_post(self,conn,url,args,request):
        #print("post set stuff")
        #conn.send('Content-Type: application/json\n\n')
        #conn.send('{"gott":"gott_me_kebab"}')
        
        req_lines = request.split('\n')
        #print(req_lines)
        body = ""
        body_sep = '\r\n\r\n'

        if body_sep in request:
            
            body_len = 0
            for lin in req_lines:
                if 'Content-Length' in lin:
                    body_len = int(lin.split(':')[1])
                    break 
            
            #print("Body len " + str(body_len))



            body = request.split(body_sep)[1]

            extra_rec = body_len - len(body)
            #print("Recieveing extra " + str(extra_rec))
            req_bytes = conn.recv(extra_rec)
            body += req_bytes.decode("utf-8") 
            #body = body.strip()



      
        if len(body)>0 and False:
            print("Body")
            print(body)
        obj = {}
        try:
            #body = body.replace('\n','')
            obj = json.loads(body)
        except:
            print("Failed to parse JSON from server")
            resp = {'status':'not gud'}
        
        try:
            resp = self._post_callback(obj)
        except Exception as e:
            print("Failed to run post callback")
            print(e)
            raise e
            resp = {'status':'gud'}


        resp_json = json.dumps(resp)
        print(resp_json)

        conn.send('Connection: close\n')
        conn.send('Content-Type: application/json\n\n')
        
        conn.send(resp_json)



def get_callback():
    print("GET CALLBACK")

    return {"kebab_lvl":13337, "svarv_lvlv":10009009420, "rgb":"fett"}

def post_callback(args):
    print("POST CALLBACK")
    print(args)

    return {"status":'glenn'}

glenn = 1

if __name__ == '__main__':

    print("connecting to wifi")
    connect_wifi()
    print("starting server")
    server = HttpServer(get_callback,post_callback)
    print("LEESGO")
    server.start_server()
    server._server_thread()

