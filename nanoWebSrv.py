import socket
import time
import json
import gc

class NANOWEBSRV:
    def __init__(self, html=None):
        gc.enable()
        ## enable debug print statements
        self.debug = True
        self.debug_level = 'relaxed' # verbose and relaxed

        ## set port
        port = 80

        ## initiate listening socket server
        addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]
        self.s = socket.socket()
        self.s.bind(addr)
        self.s.listen(5)
        self.s.settimeout(None)
        if(self.debug and self.debug_level == 'relaxed'):
            print('listening on', addr)

    def changeHTML(self, new_html):
        f = open(new_html, "r")
        self.html = str(f.read())
        f.close()

    def socketListener(self):
        gc.collect()
        cl, addr = self.s.accept()
        if(self.debug and self.debug_level == 'relaxed'):
            print('client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        client_ask = open('client_response.txt', 'w')
        while True:
            line = cl_file.readline()
            client_ask.write(line)
            if not line or line == b'\r\n':
                break
        client_ask.close()
        client_dict = self.getClientAsk(client_ask)
        self.getRoute(cl, client_dict)
        cl.close()
        if(self.debug and self.debug_level == 'verbose'):
            print(client_ask)

    def getRoute(self, client, client_dict):
        gc.collect()
        url = client_dict["Method"]
        method_type = str(url).split('/')[0][:-1].lower()
        uri = str(str(url).split('/')[1]).replace(' HTTP', '').lower()
        if(self.debug and self.debug_level == 'relaxed'):
            print(uri)
        
        Maximum_segment_size = 536
        try:
            if(method_type == 'get' and uri == 'favicon.ico'):
                f = open('www/favicon.ico', 'rb')
            elif(method_type == 'get' and uri == 'circuit-specialists-logo.png'):
                f = open('www/circuit-specialists-logo.png', 'rb')
            elif(method_type == 'get' and uri == ''):
                f = open('www/index.html', 'rb')
            elif(method_type == 'get' and uri == 'setwifi'):
                f = open('www/setwifi.html', 'rb')
            else:
                f = open('www/error.html', 'rb')
            response = f.read(Maximum_segment_size)
            while (len(response) > 0):
                client.send(response)
                response = f.read(Maximum_segment_size)
            f.close()
        except Exception as e:
            print(e)
            client.sendall("<!DOCTYPE html><html><body><h1>Server Error</h1><p>Server Error.</p></body></html>")

    def getClientAsk(self, client_ask):
        f = open('client_response.txt','r', encoding='utf-16')
        temp = f.read()
        f.close()
        try:
            temp = temp.replace('\r\n\r\n', '').replace('\r\n', '\", \"').replace(': ', '\": \"')
            client_dict = json.loads("{ \"Method\": \"" + temp + "\" }")
            return client_dict
        except Exception as e:
            print(e)