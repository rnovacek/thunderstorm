import os
import sys
import time
import math

try:
    from random import randrange, random, choice
except ImportError:
    from uos import urandom

    def random():
        n = urandom(4)
        return (n[0] + n[1] * 256 + n[2] * 256 * 256 + n[3] * 256 * 256 * 256) / (256 ** 4)

    def randrange(start, stop=None):
        if stop is None:
            stop = start
            start = 0

        return int(start + (stop - start) * random())

    def choice(seq):
        return seq[int(random() * len(seq))]


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
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(True)

    if config.USE_AP:
        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)

        print('connecting to network...')
        start_time = time.time()
        sta_if.connect(config.SSID, config.PASSWORD)
        while not sta_if.isconnected() and time.time() - start_time < 3.0:
            pass
        print('network config:', sta_if.ifconfig())
    print('AP network config:', ap_if.ifconfig())

if is_embedded:
    import webrepl
    webrepl.start()

pin = Pin(config.NEOPIXEL_PIN, Pin.OUT)
count = config.NEOPIXEL_COUNT
np = NeoPixel(pin, count)


@WebApp.register('stop')
def stop():
    pass


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
def blue():
    for i in range(count):
        np[i] = (0, 0, 255)
    np.write()

@WebApp.register('yellow')
def yellow():
    for i in range(count):
        np[i] = (255, 255, 0)
    np.write()
    
@WebApp.register('fuchsia')
def fuchsia():
    for i in range(count):
        np[i] = (255, 0, 255)
    np.write()

@WebApp.register('white')
def white():
    for i in range(count):
        np[i] = (255, 255, 255)
    np.write()

def gauss(a, b, c, x):
    return a * math.exp(-((x - b) ** 2.0) / (2 * (c ** 2.0)))


@WebApp.register('lightning')
def lightning():
    i = 0
    increment = 0.5

    colors = []
    while i < 12:
        i += increment
        v = _lightning(1.0, 2.0, i) + _lightning(0.75, 7.0, i) + _lightning(0.5, 9.0, i)
        colors.append((v, v, v))

    for color in colors:
        for j in range(count):
            np[j] = color
        np.write()
        yield 10
    off()


def _lightning(amplitude, offset, index):
    return max(0, int(255 * (gauss(amplitude, offset, 1.25, index))))


@WebApp.register('storm')
def storm():
    increment = 0.5
    segment = config.NEOPIXEL_SEGMENTS[0]

    while True:
        i = 0
        if choice((1, 2, 3, 4)) < 4:
            segment = choice(config.NEOPIXEL_SEGMENTS)
        amplitude = choice((1.0, 0.75, 0.5))
        duration = choice((3.0, 5.0, 8.0))

        while i < duration:
            i += increment
            v = _lightning(amplitude, 0, i)
            for j in range(config.NEOPIXEL_COUNT):
                if j in segment:
                    np[j] = (v, v, v)
                else:
                    np[j] = (10, 10, 10)
            np.write()
            yield 25


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
            yield 1
            if changing_color[2] == 255:
                break
        while True:
            changing_color[1] += 1
            changing_color[2] -= 1
            for i in range(count):
                np[i] = changing_color
            np.write()
            yield 1
            if changing_color[1] == 255:
                break
        while True:
            changing_color[0] += 1
            changing_color[1] -= 1
            for i in range(count):
                np[i] = changing_color
            np.write()
            yield 1
            if changing_color[0] == 255:
                break


@WebApp.register('blik')
def blik():
    while True:
        for color in [red, blue, green]:
            color()
            yield 2000

def run(func):
    result = func()
    for wait in result:
        time.sleep_ms(wait)
        

if __name__ == '__main__':
    connect()
    WebApp().start(default_func=storm)
