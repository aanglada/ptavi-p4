#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""
import sys
import json
import socketserver
from datetime import datetime, date, time, timedelta

if len(sys.argv) != 2:
    sys.exit('Usage: python3 server.py port')


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    dicc = {}

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        self.json2registered()
        mess = []
        for line in self.rfile:
            mess.append(line.decode('utf-8'))
        message = mess[0]
        expires = mess[1].split('\r\n')[0].split(': ')[1]
        metodo = message.split(' ')[0]
        user = message.split(' ')[1].split(':')[1]
        if int(expires) == 0:
            try:
                del self.dicc[user]
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                print(user + ' eliminado')
            except KeyError:
                self.expires()
        else:
            address = self.client_address[0] + ':' + str(self.client_address[1])
            expires_time = (datetime.now() + timedelta(seconds=int(expires))).strftime('%H:%M:%S %d-%m-%Y')
            self.dicc[user] = {'address': address, 'expires': expires_time}
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            print(str.upper(metodo) + ' recibido de ' + user)
        self.registered2json()

    def expires(self):
        now = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
        del_list = []
        for usuario in self.dicc:
            if now >= self.dicc[usuario]['expires']:
                del_list.append(usuario)
        for user in del_list:
            del self.dicc[user]

    def registered2json(self):
        with open('registered.json', 'w') as jsonfile:
            json.dump(self.dicc, jsonfile, indent=3)

    def json2registered(self):
        self.expires()
        try:
            with open('registered.json', 'r') as jsonfile:
                self.dicc = json.load(jsonfile)
        except:
            pass

if __name__ == "__main__":

    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
