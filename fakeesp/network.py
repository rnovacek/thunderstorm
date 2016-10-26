"""
Placeholder file to simulate ESP8266 Micropython API on computer, do NOT install into the ESP device!
"""


STA_IF = 1


class WLAN:
    def __init__(self, mode):
        self._mode = mode
        self._active = False
        self._connected = False

    def active(self, active):
        self._active = active

    def isconnected(self):
        return self._connected

    def connect(self, ssid, password):
        self._connected = True

    def ifconfig(self):
        return "<fake connection>"
