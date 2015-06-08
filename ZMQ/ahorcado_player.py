#!/usr/bin/python
# -*- coding: utf-8 -*-
import zmq
import time

from ahorcado_funciones import *

context = zmq.Context()
socket = context.socket(zmq.REP)

puerto = obtener_puerto()
print "### EL JUEGO DEL AHORCADO ###"
print "Reglas: debe adivinar la frase que se le propone contestando con letras, palabras "
print "o la frase entera si lo desea. Ganará el que adivine antes la frase.\n"
print "Su puerto es el", puerto, ".\n"
print "Aguarde su turno...\n"
socket.bind("tcp://*:" + puerto)

while True:
    message = socket.recv()
    if message == "-1":
        print "Lo siento, has perdido."
        break
    else:
        print "FRASE A ADIVINAR: ", message
        respuesta = raw_input("Su turno. Introduzca una letra, palabra o la frase entera: ") 
        socket.send(respuesta)
        oculta = socket.recv() # Recibe la cadena que se intenta adivinar.
        print "RESPUESTA: ", lista_a_cadena(oculta)
        socket.send("Recibido")
        if lista_a_cadena(oculta).find('_')!=-1:
            print "Aun no se conoce la respuesta. Aguarde su turno..."
        else:
            print "Felicidades, ha adivinado la frase!"
            break
