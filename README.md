Thunderstorm with LED diodes and ESP8266
===

This repository contains source code for a little project to create a thunderstorm using cotton wool clouds, LED strip and ESP8266 microcontroller.

Installation
---

1) create `config.py` with following structure

```
USE_AP = False  # set to True to connect to external network, default AP from ESP will be used if False
SSID = ''  # SSID of network you want to connect to
PASSWORD = ''  # Password of the network
NEOPIXEL_PIN = 5  # pin of ESP where is the NeoPixel strip connected
NEOPIXEL_COUNT = 30  # number of LEDs on the NeoPixel strip
```

2) install requirements (you may want to use virtualenv), specifically you'll need `mpfshell` command

```
pip install requirements.txt
```

3) connect ESP8266, [download](https://micropython.org/download#esp8266) and [install](https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html#deploying-the-firmware) MicroPython to it (if you don't have it already)

4) check ESP8266 port and if it's different from `/dev/ttyUSB0`, change it in `upload.mpf` file

5) upload files to ESP8266 using `mpfshell`

```
mpfshell -s upload.mpf
```

6) reboot the ESP

7) connect to IP address of the ESP from your browser and select mode

8) enjoy!
