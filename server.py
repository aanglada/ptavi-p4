#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""
import sys
import socketserver

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
                pass
        else:
            self.diccionario[user] = [self.client_address[0], expires]
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            print(str.upper(metodo) + ' recibido de ' + user)

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
