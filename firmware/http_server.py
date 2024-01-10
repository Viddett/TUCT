
import time,network
import wifi_creds
import json
import index

try:
    import uasyncio as asyncio
except:
    import asyncio

try:
    import usocket as socket
except:
    import socket

APPLICATION_JSON = 'application/json'
TEXT_HTML = 'text/html'
OK = '200 OK'
BAD_REQUEST = '400 Bad request'
CREATED = '201 Created'


def start_wifi(timeout_s:int=9):

    #wlan = network.WLAN(network.STA_IF) #initialize the wlan object
    wlan = network.WLAN(network.AP_IF)
    wlan.config(essid=wifi_creds.wifi_ssid, password= wifi_creds.wifi_pswd)
    wlan.active(True)

    wlan.config(pm = 0xa11140)


    wait_time = 0
    while not wlan.active():
        print("Waiting to start wifi...")
        time.sleep(1)
        wait_time += 1

        if wait_time > timeout_s:
            raise Exception("Failed to connect to wifi!")

    print(wlan.ifconfig())


#  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating socket object
#    s.bind(('', 80))
#    s.listen(5)

class HttpServer:

    def __init__(self, get_state_callback, post_callback):
        self._get_callback = get_state_callback
        self._post_callback = post_callback
        self._stop_flag = False

        self._html_response = index.html

    async def socket_handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info('peername')
        print(f'Got a connection from {addr}.')

        data: bytes = await reader.read(1024)
        request = data.decode('utf-8')

        print(f'Message received: \n {request}')

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
            await self.write_response(writer,OK)

        elif method == 'GET':
            await self._handle_get_2(writer,url,args,request)

        elif method == 'POST':
            await self._handle_post_2(writer,url,args,request,reader)

        else:
            await self._send_bad_req_2(writer)

        print('Closing connection...')
        writer.close()
        await writer.wait_closed()
        print('Connection closed.')

    async def _send_bad_req_2(self,writer: asyncio.StreamWriter):
            to_send = ['HTTP/1.1 400 Bad Request\n',
                       'Content-Type: text/html\n',
                       'Connection: close\n',
                       '\n',
                       index.html_bad_request]
            for line in to_send:
                writer.write(line)
                await writer.drain()

    async def _handle_get_2(self,writer: asyncio.StreamWriter,url:str,args,request):
        if url == '/':
            # Default landing page
            await self.write_response(writer,OK,TEXT_HTML,self._html_response)
        elif url == '/state':
            # return tree state as json
            state = self._get_callback()
            state_json = json.dumps(state)
            await self.write_response(writer,OK,APPLICATION_JSON,state_json)
        else:
            # Bad request
            await self._send_bad_req_2(writer)

    async def _handle_post_2(self,writer: asyncio.StreamWriter,url,args,request:str,reader:asyncio.StreamReader):
        req_lines = request.split('\n')
        body = ""
        body_sep = '\r\n\r\n'

        if body_sep in request:

            body_len = 0
            for line in req_lines:
                if 'Content-Length' in line:
                    body_len = int(line.split(':')[1])
                    break

            body = request.split(body_sep)[1]

            extra_rec = body_len - len(body)
            if extra_rec > 0:
                req_bytes: bytes = await reader.read(extra_rec)
                body += req_bytes.decode("utf-8")

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

        await self.write_response(writer,CREATED,APPLICATION_JSON,resp_json)

    @staticmethod
    async def write_response(writer: asyncio.StreamWriter,code:str,content_type:str='',body:str=''):
        to_send = [f'HTTP/1.1 {code}',
                    "Access-Control-Allow-Origin: *",
                    "Access-Control-Allow-Credentials : true",
                    "Access-Control-Allow-Methods : GET,HEAD,OPTIONS,POST,PUT",
                    "Access-Control-Allow-Headers:Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers",
                    'Connection: close']

        if content_type != '':
            to_send.append(f'Content-Type: {content_type}')

        if body != '':
            to_send.append('')
            to_send.append(body)

        for message in to_send:
            writer.write(message + '\n')
            await writer.drain()


def get_callback():
    print("GET CALLBACK")

    return {"kebab_lvl":13337, "svarv_lvlv":10009009420, "rgb":"fett"}

def post_callback(args):
    print("POST CALLBACK")
    print(args)

    return {"status":'glenn'}

glenn = 1

async def start_all():
    server = HttpServer(get_callback,post_callback)
    await asyncio.start_server(server.socket_handler, '0.0.0.0', 80)
    print("LEESGO")
    loop = asyncio.get_event_loop()
    loop.run_forever()

if __name__ == '__main__':

    print("starting wifi")
    start_wifi()
    print("starting server")
    asyncio.run(start_all())
