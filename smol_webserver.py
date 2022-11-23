from machine import Pin
import time, network, _thread
import wifi_creds


try:
  import usocket as socket
except:
  import socket


led = Pin("LED", Pin.OUT)
_ledStatus = False


def connect_to_wifi(wlan):
    # set power mode to get WiFi power-saving off (if needed)
    # fuk powe save
    wlan.config(pm = 0xa11140)

    wlan.connect(wifi_creds.wifi_ssid, wifi_creds.wifi_pswd)

    while not wlan.isconnected() and wlan.status() >= 0:
        print("Waiting to connect:")
        time.sleep(1)

    print(wlan.ifconfig())


def getLedStatus():
  global _ledStatus
  lock = _thread.allocate_lock()
  with lock:
    return _ledStatus


def setLedStatus(status):
  print('LED', status)
  global _ledStatus
  lock = _thread.allocate_lock()
  with lock:
    _ledStatus = status
    led.value(status)


def startNet():
  print("Starting net")
  wlan = network.WLAN(network.STA_IF) #initialize the wlan object
  wlan.active(True) #activates the wlan interface
  connect_to_wifi(wlan)
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(('', 80))
  s.listen(5)
  print("Wifi initialized, waiting for requests..")
  while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)
    led_on = request.find('/?led=on')
    led_off = request.find('/?led=off')
    if led_on == 6:
      setLedStatus(True)
    if led_off == 6:
      setLedStatus(False)
    response = "Gött med kebab"
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
