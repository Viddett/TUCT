
import time,network
import wifi_creds

#try:
#    import usocket as socket
#except:
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


HOST = "192.168.0.13"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

def socketClient():
    while True:
        try:
            print("do socketClient")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            msg_id = 1
            string = "message string"
            msg_len = string.__sizeof__
            s.sendall(b"Hello, world")
            data = s.recv(1024)
        
        except:
            print("failed, retry")


def main():
    print("connecting to wifi")
    connect_wifi()
    print("connected to wifi")
    socketClient()