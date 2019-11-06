import socket
import time
import json

class NANOWEBSRV:
    def __init__(self, html=None):
        ## enable debug print statements
        self.debug = True

        ## set port
        port = 80

        ## load default index.html, unless specified
        if(html == None):
            try:
                f = open("index.html", "r")
                self.html = str(f.read())
                f.close()
            except Exception as e:
                print("Index.html does not exist")
                raise
        else:
            self.html = html

        ## initiate listening socket server
        addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]
        self.s = socket.socket()
        self.s.bind(addr)
        self.s.listen(5)
        self.s.settimeout(None)
        if(self.debug):
            print('listening on', addr)

    def changeHTML(self, new_html):
        f = open(new_html, "r")
        self.html = str(f.read())
        f.close()

    def socketListener(self):
        cl, addr = self.s.accept()
        if(self.debug):
            print('client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        client_ask = open('client_response.txt', 'w')
        while True:
            line = cl_file.readline()
            client_ask.write(line)
            if not line or line == b'\r\n':
                break
        client_ask.close()
        self.getClientAsk(client_ask)
        #self.getRoute(client_ask)
        response = self.html
        cl.sendall(response)
        cl.close()
        if(self.debug):
            #print(client_ask)
            print()

    def getRoute(self, client_ask):
        print()

    def getClientAsk(self, client_ask):
        f = open('client_response.txt','r', encoding='utf-16')
        temp = f.read()
        f.close()
        try:
            temp = temp.replace('\r\n\r\n', '').replace('\r\n', '\", \"').replace(': ', '\": \"')
            self.client_dict = json.loads("{ \"Method\": \"" + temp + "\" }")
            print(self.client_dict)
        except Exception as e:
            print(e)