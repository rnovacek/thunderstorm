"""
Placeholder file to simulate ESP8266 Micropython API on computer, do NOT install into the ESP device!
"""


class Pin(object):
    OUT = 1

    def __init__(self, port, direction):
        self._value = 0

    def value(self, v=None):
        if v is None:
            return self._value
        else:
            print("setting value to", v)
            self._value = v


class PWM(object):
    def __init__(self, pin):
        self._pin = pin
        self._duty = 0
        self._freq = 500

    def duty(self, v=None):
        if v is None:
            return self._duty
        else:
            print("setting duty to", v)
            self._duty = v

    def freq(self, v=None):
        if v is None:
            return self._freq
        else:
            print("setting freq to", v)
            self._freq = v


print("Using fake machine module, do NOT use on the device!")
