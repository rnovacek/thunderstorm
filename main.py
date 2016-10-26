import os
import sys
import time
import math

from webapp import WebApp

is_embedded = sys.platform == 'esp8266'

if not is_embedded:
    # use fake libraries to simulate ESP
    sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fakeesp'))

    
from neopixel import NeoPixel
from machine import Pin
import network

if not hasattr(time, 'sleep_ms'):
    # CPython doesn't have sleep_ms but micropython does, monkeypatch it
    time.sleep_ms = lambda t: time.sleep(t / 1000.0)


try:
    import config
except ImportError:
    print("Create config not found, see README")
    sys.exit(1)
    
def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(config.SSID, config.PASSWORD)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

if is_embedded:
    import webrepl
    webrepl.start()

pin = Pin(config.NEOPIXEL_PIN, Pin.OUT)
count = config.NEOPIXEL_COUNT
np = NeoPixel(pin, count)


@WebApp.register('off')
def off():
    for i in range(count):
        np[i] = (0, 0, 0)
    np.write()


@WebApp.register('red')
def red():
    for i in range(count):
        np[i] = (255, 0, 0)
    np.write()


@WebApp.register('green')
def green():
    for i in range(count):
        np[i] = (0, 255, 0)
    np.write()

@WebApp.register('blue')
def green():
    for i in range(count):
        np[i] = (0, 0, 255)
    np.write()


def gauss(a, b, c, x):
    return a * math.exp(-((x - b) ** 2.0) / (2 * (c ** 2.0)))

@WebApp.register('lightning')
def lightning():
    i = 0
    increment = 0.5
    while i < 12:
        i += increment
        v = max(0, int(255 * (gauss(1.0, 2.0, 1.25, i) + gauss(0.75, 7.0, 1.25, i) + gauss(0.5, 9.0, 1.25, i))))
        for j in range(count):
            np[j] = (v, v, v)
        np.write()
        time.sleep_ms(1)
    off()

if __name__ == '__main__':
    if config.USE_AP:
        connect()
    lightning()
    WebApp().start()
