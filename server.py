#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""
import sys
import socketserver


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
        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")

        for line in self.rfile:
            mess = line.decode('utf-8')
            if len(mess.split(' ')) != 1:
                metodo = mess.split(' ')[0]
                user = mess.split(' ')[1]
                self.diccionario[user] = self.client_address[0]
                print(str.upper(metodo) + ' recibido')

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
