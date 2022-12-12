# Micropython firmware for TUCT 2k22

Currently using micro-python, check here for some refs: 
* https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf
* https://datasheets.raspberrypi.com/picow/connecting-to-the-internet-with-pico-w.pdf
* https://docs.micropython.org/en/latest/rp2/quickref.html
* https://docs.micropython.org/en/latest/library/rp2.html

## Setup Micropython on Pico-W
1. Download `uf2` img from https://micropython.org/download/rp2-pico-w/
Version `v1.19.1-643-g71881116e (2022-11-10).uf2` is known to be working.
2. Plug in the Pico and it should apear as a thumb-dribe, drop the `uf2` file there and it should restart and appear as a `COM port`
2. Install `Pico-W-Go` extension to Vs-Code (paulober.pico-w-go).
3. Open TUCT folder
4. In Vs Code terminal (ctrl+shift+p), run "Pico-W-Go > Configure Project"
5. Click connect in the blue bottom ribbon
6. Right click .py file and press "Upload to project"
7. Run code with "Run" in the blue bottom ribbon

## Wifi-credentials
Currently we can connect to wifi, but to avoid pushing our wifi-credentials. You
should declare them in a file `wifi_creds.py` as 

```python
wifi_ssid =  'Winternet is Coming'
wifi_pswd = 'justtypesomethingmaybefart123'
```

which can be used in the main script as

```python
import wifi_creds

wlan.connect(wifi_creds.wifi_ssid, wifi_creds.wifi_pswd)
```
**DO NOT COMMIT THE `wifi_creds.py` FILE!**

## File structure
`http_server.py` - Implements a http-server with api-endpoints for reading and writing to the tree.
`index.py` - Container for the HMTL when someone makes get request with a browser to the tree.
`smol_webserver.py` - Old, to be removed
`testPico.py` - Test script to test if pico is alive
`tuct_leds.py` - LEDlibrary to set colors of the leds, this can be run to test the leeds on the tree as well.

## API Endpoints

The `http_server.py` implements 3 http endpoints 

`GET /` - Root, returns the html defined in `index.py`

`GET /state` - Returns a json object containing the state of the tree.
Needs to be implemented by the user, see example below.

`POST /` - Sends a json object to the tree. Can be defined by the user what this object can contain.



```python
import http_server

def get_state_callbck():
    # Function that returns the tree state as a dict
    return  {"kebab_lvl":13337, "svarv_lvlv":10009009420, "rgb":"fett"}

def set_state_callbck(json_obj:dict()):
    # Function that get called when a json object is sent to the tree.

def main():
    http_server.connect_wifi()
    server = http_server.HttpServer(get_state_callbck,set_state_callbck)
    server.start_server()
```

Example of how to make a POST request from javascript

```javascript
function send_post_pico(){
	
	fetch('http://192.168.1.92/', {
    method: 'POST',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ "id": 78912 })
})
.then(response => response.json())
.then(response => console.log(JSON.stringify(response)))
}
```

