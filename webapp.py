
import sys
import socket
import gc


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
            for command in WebApp.commands:
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
        if content_type:
            headers.append('Content-Type: {}'.format(content_type))
        self._send(cl, '\r\n'.join(headers).encode('ascii'))
        self._send(cl, b'\r\n\r\n')
        self._send(cl, data)
        cl.close()

    @classmethod
    def register(cls, label):
        def outer(func):
            cls.commands[label] = func
            def inner(*args, **kwargs):
                return func(*args, **kwargs)
            return inner
        return outer

    def start(self):
        addr = socket.getaddrinfo('0.0.0.0', 80 if len(sys.argv) < 2 else sys.argv[1])[0][-1]

        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(1)

        print('listening on', addr)

        while True:
            cl, addr = s.accept()
            print('client connected from', addr)
            cl_file = cl.makefile('rwb', 0)
            first_line = cl_file.readline().decode('ascii')
            while True:
                line = cl_file.readline()
                if not line or line == b'\r\n':
                    break
            print(first_line)
            method, path, protocol = first_line.split(' ')
            if method.lower() == 'get':
                if path == '/':
                    self.send(cl, 200, filename='index.html', content_type='text/html; charset=utf-8')
                else:
                    self.send(cl, 404)
            elif method.lower() == 'post':
                try:
                    func = WebApp.commands[path.lstrip('/')]
                except KeyError:
                    self.send(cl, 404)
                    return
                func()
                self.send(cl, 200)

            #mem = gc.mem_alloc()
            #gc.collect()
            #print("Freeing", mem - gc.mem_alloc(), "now free", gc.mem_free())
