import socket
import time

class WEBSRV:
    def __init__(self):
        import uos
        files = uos.listdir()
        if("creds.txt" in files):
            f = open("index.html", "r")
            self.html = str(f.read())
            f.close()
        else:
            f = open("creds.html", "r")
            self.html = str(f.read())
            f.close()

        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

        self.s = socket.socket()
        self.s.bind(addr)
        self.s.listen(1)

        print('listening on', addr)

    def socketListener(self):
        cl, addr = self.s.accept()
        print('client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break
        response = self.html
        while len(response) > 0:
            cl.send(response[:536])
            response = response[536:]
            time.sleep(.2)
        cl.close()
