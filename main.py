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
    print("Config not found, see README for instructions how to create one")
    sys.exit(1)


def connect():
    mode = network.STA_IF if config.USE_AP else network.AP_IF

    wlan = network.WLAN(mode)
    wlan.active(True)
    if config.USE_AP and not wlan.isconnected():
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

@WebApp.register('rainbow')
def rainbow():
    changing_color = [255, 0, 0]
    while True:
        while True:
            changing_color[2] += 1
            changing_color[0] -= 1
            for i in range(count):
                np[i] = changing_color
            np.write()
            if changing_color[2] == 255:
                break
        while True:
            changing_color[1] += 1
            changing_color[2] -= 1
            for i in range(count):
                np[i] = changing_color
            np.write()
            if changing_color[1] == 255:
                break
        while True:
            changing_color[0] += 1
            changing_color[1] -= 1
            for i in range(count):
                np[i] = changing_color
            np.write()
            if changing_color[0] == 255:
                break

        '''
        while np[i][2] <= 255:
            np[i] = (np[i][0]-1, 0, np[i][2]+1)
            time.sleep_ms(20)
            np.write()
        while np[i][1] <= 255:
            for i in range(count):
                np[i] = (0, np[i][1]+1, np[i][2]-1)
                time.sleep_ms(20)
                np.write()
        while np[i][0] <= 255:
            for i in range(count):
                np[i] = (np[i][0]+1, np[i][1]-1, 0)
                time.sleep_ms(20)
                np.write()
        '''




if __name__ == '__main__':
    connect()
    lightning()
    WebApp().start()
