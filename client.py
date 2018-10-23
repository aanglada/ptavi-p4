#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import socket
import sys

if len(sys.argv) != 6:
    sys.exit('Usage: client.py ip puerto register sip_address expires_value')

# Constantes. Dirección IP del servidor y contenido a enviar
SERVER = sys.argv[1]
PORT = int(sys.argv[2])
MESSTYPE = sys.argv[3]
USER = sys.argv[4]
EXPIRES = int(sys.argv[5])

MESSAGE = str.upper(MESSTYPE) + ' sip:' + USER + ' SIP/2.0\r\n' + 'Expires: ' + str(EXPIRES) + '\r\n\r\n'

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, PORT))
    print(MESSAGE)
    my_socket.send(bytes(MESSAGE, 'utf-8'))
    data = my_socket.recv(1024)
    print(data.decode('utf-8'))

print("Socket terminado.")
