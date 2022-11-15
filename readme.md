# TUCT 2k22
*The Ultimate Cristmas Tree*

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

