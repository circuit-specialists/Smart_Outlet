"""
   written by Mitch Zakocs from CircuitSpecialists.com
   licensed as GPLv3
"""

import socket
import time
import json
import gc
import smart_control
import ubinascii
import uos

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
        self.disable = False

    def changeHTML(self, new_html):
        f = open(new_html, "r")
        self.html = str(f.read())
        f.close()

    def socketListener(self):
        gc.collect()
        if self.disable == False:
            cl, addr = self.s.accept()
            if(self.debug):
                print('client connected from', addr)
            cl_file = cl.makefile('rwb', 1)
            client_ask = open('client_response.txt', 'w')
            while True:
                line = cl_file.readline()
                client_ask.write(line)
                if not line or line == b'\r\n':
                    break
            client_ask.close()
            client_dict = self.getClientAsk()
            self.getRoute(cl, client_dict)
            cl.close()
            if(self.debug and self.debug_level == 'verbose'):
                print("JSON Dict: %s" % client_dict)

    def getRoute(self, client, client_dict):
        gc.collect()
        url = client_dict["Method"]
        method_type = str(url).split('/')[0][:-1].lower()
        uri_nolower = str(str(url).split('/')[1]).replace(' HTTP', '')
        uri = uri_nolower.lower()
        if(self.debug and self.debug_level == 'relaxed'):
            print("URI: %s" % uri)
        elif(self.debug and self.debug_level == 'verbose'):
            print("URL: %s" % url)
            print("URI: %s" % uri)
            print("JSON Dict: %s" % client_dict)


        ## Set captive portal condition
        files = uos.listdir()
        if("creds.txt" not in files):
            captive_portal = True
        else:
            captive_portal = False
        
        Maximum_segment_size = 536
        relayControl = smart_control.CONTROLLER()
        try:
            if('.' in uri):
                if(uri[:10] == 'creds.html'):
                    #Gets rid of the % signs in the URI
                    uri_nolower = self.special_char_digest(uri_nolower)
                    #Gets the SSID and Password from the URI
                    ssid = self.uriParse('SSID=', uri_nolower)
                    password = self.uriParse('password=', uri_nolower)
                    #Writes the SSID and Password to the credentials text file
                    f = open('creds.txt', 'wb')
                    f.write(str(ssid) + '\n')
                    f.write(str(password))
                    f.close()
                    #Opens the creds success webpage
                    f = open('www/creds.html', 'rb')
                elif (uri[:16] == 'scheduleset.html'):
                    #Gets rid of the % signs in the URI
                    uri_nolower = self.special_char_digest(uri_nolower)
                    #Gets all of the needed time values from the URI
                    mondayV = self.uriParse('Mo_V=', uri_nolower)
                    mondayON = self.uriParse('Mo_ON=', uri_nolower)
                    mondayOFF = self.uriParse('Mo_OFF=', uri_nolower)
                    tuesdayV = self.uriParse('Tu_V=', uri_nolower)
                    tuesdayON = self.uriParse('Tu_ON=', uri_nolower)
                    tuesdayOFF = self.uriParse('Tu_OFF=', uri_nolower)
                    wednesdayV = self.uriParse('We_V=', uri_nolower)
                    wednesdayON = self.uriParse('We_ON=', uri_nolower)
                    wednesdayOFF = self.uriParse('We_OFF=', uri_nolower)
                    thursdayV = self.uriParse('Th_V=', uri_nolower)
                    thursdayON = self.uriParse('Th_ON=', uri_nolower)
                    thursdayOFF = self.uriParse('Th_OFF=', uri_nolower)
                    fridayV = self.uriParse('Fr_V=', uri_nolower)
                    fridayON = self.uriParse('Fr_ON=', uri_nolower)
                    fridayOFF = self.uriParse('Fr_OFF=', uri_nolower)
                    saturdayV = self.uriParse('Sa_V=', uri_nolower)
                    saturdayON = self.uriParse('Sa_ON=', uri_nolower)
                    saturdayOFF = self.uriParse('Sa_OFF=', uri_nolower)
                    sundayV = self.uriParse('Su_V=', uri_nolower)
                    sundayON = self.uriParse('Su_ON=', uri_nolower)
                    sundayOFF = self.uriParse('Su_OFF=', uri_nolower)
                    # If the file already exists, don't overwrite if the value is blank for the scheduling option
                    # This is so you don't have to completely re-enter all of your times every time you set the schedule, you can just update it
                    files = uos.listdir()
                    if ("schedule.txt" in files):
                        f = open('schedule.txt', 'r')
                        line = f.readlines()
                        #Reads and overwrites the previous values if the schedule value is set to 0
                        if (mondayV == '0'):
                            mondayV = str(line[0]).strip('\n')
                            mondayON = str(line[1]).strip('\n')
                            mondayOFF = str(line[2]).strip('\n')
                        if (tuesdayV == '0'):
                            tuesdayV = str(line[3]).strip('\n')
                            tuesdayON = str(line[4]).strip('\n')
                            tuesdayOFF = str(line[5]).strip('\n')
                        if (wednesdayV == '0'):
                            wednesdayV = str(line[6]).strip('\n')
                            wednesdayON = str(line[7]).strip('\n')
                            wednesdayOFF = str(line[8]).strip('\n')
                        if (thursdayV == '0'):
                            thursdayV = str(line[9]).strip('\n')
                            thursdayON = str(line[10]).strip('\n')
                            thursdayOFF = str(line[11]).strip('\n')
                        if (fridayV == '0'):
                            fridayV = str(line[12]).strip('\n')
                            fridayON = str(line[13]).strip('\n')
                            fridayOFF = str(line[14]).strip('\n')
                        if (saturdayV == '0'):
                            saturdayV = str(line[15]).strip('\n')
                            saturdayON = str(line[16]).strip('\n')
                            saturdayOFF = str(line[17]).strip('\n')
                        if (sundayV == '0'):
                            sundayV = str(line[18]).strip('\n')
                            sundayON = str(line[19]).strip('\n')
                            sundayOFF = str(line[20]).strip('\n')
                        f.close()
                    #Writes the needed time values to the schedule text file
                    f = open('schedule.txt', 'w')
                    f.write(str(mondayV) + '\n' + str(mondayON) + '\n' + str(mondayOFF) + '\n')
                    f.write(str(tuesdayV) + '\n' + str(tuesdayON) + '\n' + str(tuesdayOFF) + '\n')
                    f.write(str(wednesdayV) + '\n' + str(wednesdayON) + '\n' + str(wednesdayOFF) + '\n')
                    f.write(str(thursdayV) + '\n' + str(thursdayON) + '\n' + str(thursdayOFF) + '\n')
                    f.write(str(fridayV) + '\n' + str(fridayON) + '\n' + str(fridayOFF) + '\n')
                    f.write(str(saturdayV) + '\n' + str(saturdayON) + '\n' + str(saturdayOFF) + '\n')
                    f.write(str(sundayV) + '\n' + str(sundayON) + '\n' + str(sundayOFF) + '\n')
                    f.close()
                    #Opens the scheduleset webpage
                    f = open ('www/scheduleset.html', 'rb')
                elif(uri == 'favicon.ico'):
                    f = open('www/favicon.ico', 'rb')
                elif(uri == 'circuit-specialists-logo.png'):
                    f = open('www/circuit-specialists-logo.png', 'rb')
                else:
                    f = open('www/error.html', 'rb')
            elif(captive_portal):
                f = open('www/setwifi.html', 'rb')
            else:
                ## set uri handling
                if(uri == ''):
                    f = open('www/index.html', 'rb')
                elif(uri == 'setwifi'):
                    f = open('www/setwifi.html', 'rb')
                elif(uri == 'started'):
                    f= open('www/started.html', 'rb')
                    self.disable = True
                elif(uri == 'relayon'):
                    relayControl.turnON()
                    f = open('www/success.html', 'rb')
                elif(uri == 'relayoff'):
                    relayControl.turnOFF()
                    f = open('www/success.html', 'rb')
                else:
                    f = open('www/error.html', 'rb')

            if(method_type == 'get'):
                response = f.read(Maximum_segment_size)
                if('%s' in response):
                    response = response % (ssid, password)
                while (len(response) > 0):
                    client.send(response)
                    response = f.read(Maximum_segment_size)
                f.close()
            elif(method_type == 'post'):
                receive = client.read(Maximum_segment_size)
                while (len(receive) > 0):
                    f.write(receive)
                    receive = client.read(Maximum_segment_size)
                f.close()
                client.sendall("<!DOCTYPE html><html><body><h1>Received Message</h1><p>Message Received</p></body></html>")
        except Exception as e:
            if(self.debug):
                print(e)
            client.sendall("<!DOCTYPE html><html><body><h1>Server Error</h1><p>Server Error.</p></body></html>")

    def getClientAsk(self):
        f = open('client_response.txt','r', encoding='utf-16')
        temp = f.read()
        f.close()
        if(self.debug and self.debug_level == 'verbose'):
            print("Client Ask: %s" % temp)
        try:
            temp = temp.replace('\r\n\r\n', '').replace('\r\n', '\", \"').replace(': ', '\": \"')
            client_dict = json.loads("{ \"Method\": \"" + temp + "\" }")
            return client_dict
        except Exception as e:
            if(self.debug):
                print(e)

    def special_char_digest(self, string):
        ## test if string has special char
        special_char_start = string.find('%')
        ## replace all special chars with their corresponding char
        while(special_char_start != -1):
            special_char = string[special_char_start:special_char_start + 3]
            string = string.replace(special_char, ubinascii.unhexlify(special_char.replace('%', '')).decode())
            special_char_start = string.find('%')
        return string

    def uriParse(self, stringstart, uri):
        try:
            start = uri.find(stringstart) + len(stringstart)
            end = uri.find('&', start)
            return uri[start:end]  
        except Exception as e:
            print(e)