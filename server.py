#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""
import sys, json, socketserver
from datetime import datetime, date, time, timedelta

if len(sys.argv) != 2:
    sys.exit('Usage: python3 server.py port')


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    diccionario = {}
    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        mess = []
        for line in self.rfile:
            mess.append(line.decode('utf-8'))
        message = mess[0]
        expires = mess[1].split('\r\n')[0].split(': ')[1]
        metodo = message.split(' ')[0]
        user = message.split(' ')[1].split(':')[1]
        if int(expires) == 0:
            try:
                del self.diccionario[user]
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                print(user + ' eliminado')
            except KeyError:
                self.expires()
        else:
            address = self.client_address[0] + ':' + str(self.client_address[1])
            expires_time = (datetime.now() + timedelta(seconds=int(expires))).strftime('%H:%M:%S %d-%m-%Y')
            self.diccionario[user] = {'address' : address, 'expires' : expires_time}
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            print(str.upper(metodo) + ' recibido de ' + user)
        self.registered2json()

    def expires(self):
        now = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
        del_list = []
        for usuario in self.diccionario:
            if now >= self.diccionario[usuario]['expires']:
                del_list.append(usuario)
        for user in del_list:
            del self.diccionario[user]
    
    def registered2json(self):
        self.expires()
        with open('registered.json', 'w') as jsonfile:
            json.dump(self.diccionario, jsonfile, indent=3)

if __name__ == "__main__":
    # Listens at localhost ('') port 6001 
    # and calls the EchoHandler class to manage the request
    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler) 

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
