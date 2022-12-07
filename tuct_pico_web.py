import time, network, _thread
import wifi_creds

try:
    import usocket as socket
except:
    import socket




def connect_wifi(timeout_s:int):

    wlan = network.WLAN(network.STA_IF) #initialize the wlan object
    wlan.active(True)

    wlan.config(pm = 0xa11140)

    wlan.connect(wifi_creds.wifi_ssid, wifi_creds.wifi_pswd)


    wait_time = 0
    while not wlan.isconnected() and wlan.status() >= 0:
        print("Waiting to connect:")
        time.sleep(1)
        wait_time += 1

        if wait_time > timeout_s:
            raise Exception("Failed to connect to wifi!")

    print(wlan.ifconfig())



def open_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    return s

def server_loop(s):

    response = ""
    with open('index.html',encoding='utf-8') as f:
        response = f.read()
    response = response.encode()
    print(response)

    while True:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        request = str(request)
        print('Content = %s' % request)

       
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response,)
        conn.close()



if __name__ == '__main__':

    print("hheej")
    connect_wifi(9)
    print("connected yueboi")
    s = open_socket()
    print('socks on m8')
    server_loop(s)



