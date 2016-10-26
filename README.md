Thunderstorm with LED diodes and ESP8266
---

This repository contains source code for a little project to create a thunderstorm using cotton wool clouds, LED strip and ESP8266 microcontroller.

INSTALLATION
===

1) get [webrepl](https://github.com/micropython/webrepl)
2) create `config.py` with following structure

```
USE_AP = False  # set to True to connect to external network, default AP from ESP will be used if False
SSID = ''  # SSID of network you want to connect to
PASSWORD = ''  # Password of the network
NEOPIXEL_PIN = 5  # pin of ESP where is the NeoPixel strip connected
NEOPIXEL_COUNT = 30  # number of LEDs on the NeoPixel strip
```

3) upload files to ESP8266 with Micropython preloaded

```
/path/to/webrepl/webrepl_cli.py main.py network.py config.py index.html <ip_of_esp>:
```

4) reboot the ESP
5) enjoy!
