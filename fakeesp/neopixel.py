"""
Placeholder file to simulate ESP8266 Micropython API on computer, do NOT install into the ESP device!
"""


class NeoPixel:
    def __init__(self, pin, count):
        self._pin = pin
        self._count = count
        self._pixels = [(0, 0, 0) for i in range(count)]

    def __getitem__(self, index):
        return self._pixels[index]

    def __setitem__(self, index, value):
        r, g, b = value
        self._pixels[index] = (r, g, b)

    def write(self):
        for i, pixel in enumerate(self._pixels):
            print("[{}] {} {} {}".format(i, pixel[0], pixel[1], pixel[2]))
