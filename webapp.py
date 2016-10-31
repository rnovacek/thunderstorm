
import sys
try:
    import usocket as socket
except ImportError:
    usocket = None
    import socket

import gc

import time

CODE_STRINGS = {
    200: 'OK',
    404: 'Not Found',
    400: 'Bad Request',
}


class Command:
    def __init__(self, label, command):
        self.label = label
        self.command = command


class WebApp(object):
    commands = {}

    def _send(self, cl, data):
        while len(data) > 0:
            sent = cl.send(data)
            data = data[sent:]

    def send(self, cl, code, data=None, filename=None, content_type=None):
        if filename:
            with open(filename, 'r', encoding='utf-8') as f:
                data = f.read()
            buttons = []
            for command in sorted(WebApp.commands):
                buttons.append('<button data-command="{}">{}</button>'.format(command, command))
            data = data.replace("{{ buttons }}", ''.join(buttons)).encode('utf-8')
        elif not data:
            data = b''
        else:
            data = data.encode('ascii')

        headers = [
            'HTTP/1.0 {} {}'.format(code, CODE_STRINGS.get(code, '')),
            'Connection: close',
            'Content-Length: {}'.format(len(data))
        ]

        headers.append('Content-Type: {}'.format(content_type if content_type else 'text/plain'))
        self._send(cl, '\r\n'.join(headers).encode('ascii'))
        self._send(cl, b'\r\n\r\n')
        self._send(cl, data)
        cl.close()
        print('Client served:', data, code)

    @classmethod
    def register(cls, label):
        def outer(func):
            cls.commands[label] = func

            def inner(*args, **kwargs):
                return func(*args, **kwargs)
            return inner
        return outer

    def start(self, default_func=None):
        addr = socket.getaddrinfo('0.0.0.0', 80 if len(sys.argv) < 2 else sys.argv[1])[0][-1]

        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(5)

        print('listening on', addr)

        cl = None
        func = default_func
        result = None

        while True:
            if func:
                result = func()
                if not result:
                    func = None
                    continue

            # We got a generator
            for wait in result or [0]:
                s.settimeout(wait / 1000.0)
                try:
                    cl, addr = s.accept()
                    func = self.process_input(s, cl, addr) or func
                    break
                except OSError:  # BlockingIOError
                    pass

    def process_input(self, s, cl, addr):
        print('client connected from', addr)
        cl.settimeout(None)

        if not hasattr(cl, 'readline'):
            # CPython
            client_stream = cl.makefile("rwb")
        else:
            # MicroPython
            client_stream = cl

        req = client_stream.readline()
        print(req)
        while True:
            data = client_stream.readline()
            if not data or data == b'\r\n':
                break

        method, path, protocol = req.split(b' ')
        if method.lower() == b'get':
            if path == b'/':
                self.send(cl, 200, filename='index.html', content_type='text/html; charset=utf-8')
            else:
                self.send(cl, 404)
        elif method.lower() == b'post':
            try:
                func = WebApp.commands[path.lstrip(b'/').decode('ascii')]
            except KeyError:
                self.send(cl, 404)
                return
            self.send(cl, 200)
            return func
        else:
            self.send(cl, 400)

        #mem = gc.mem_alloc()
        #gc.collect()
        #print("Freeing", mem - gc.mem_alloc(), "now free", gc.mem_free())
