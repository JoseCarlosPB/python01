#!/usr/bin/python
# -*- coding: utf-8 -*-
import zmq
import random # Para generar una frase aleatoria
import re # Para actualizar la frase oculta


# Función que convierte una lista a una cadena y añade cierta expresividad.
def lista_a_cadena(lista):
    return "".join(lista)
    
    
''' FUNCIONES AUXILIARES PARA ZMQ '''

# Para ahorcado_player. Le pide un puerto a ahorcado_master.
def obtener_puerto():
    cont = zmq.Context();
    sock  = cont.socket(zmq.REQ)
    sock.connect("tcp://*:5554")
    sock.send('Recibiendo jugador')
    puerto = sock.recv()
    return puerto
    
# Para ahorcado_master. Ofrece "num_jugadores" puertos a partir del 5555
# a los jugadores que lo pidan.
def asignar_puertos(num_jugadores):
    puerto_actual = 5555 
    jugador = 0
    puertos_asignados= []
    cont = zmq.Context();
    sock = cont.socket(zmq.REP)
    sock.bind("tcp://*:5554")
    while jugador < num_jugadores:
        mensaje = sock.recv()
        print mensaje
        puerto = puerto_actual+jugador
        sock.send(str(puerto))
        puertos_asignados.append(puerto)
        jugador += 1
    return puertos_asignados

# Para ahorcado_master. Genera un socket para cada jugador, contenidos en una lista.
def generar_sockets(num_jugadores):
    contexts = []
    sockets = []
    for i in range(0, num_jugadores):
        contexts.append(zmq.Context())
        sockets.append(contexts[i].socket(zmq.REQ))
    return sockets
     
            
''' FUNCIONES AUXILIARES PARA EL JUEGO DEL AHORCADO '''

# Selecciona al azar la frase de "refranes_populares.txt" que se va a adivinar.
def frase_aleatoria():
    fichero = open("refranes_populares.txt", 'r')
    frases = fichero.readlines()
    n = len(frases)
    aleat = random.randrange(0, n)
    return frases[aleat]
    
# Dada una frase, devuelve la frase con todos sus caracteres ocultos, menos los
# espacios en blanco.
def ocultar_frase(frase):
    oculta = []
    for letra in frase:
        if letra==' ':
            oculta.append(' ')
        elif letra!='\n': # Ignoramos el salto de línea
            oculta.append('_')
    return oculta

# Actualiza la frase con la respuesta del usuario. Acepta desde letras hasta la frase entera.
def actualizar_frase_oculta(oculta, frase, respuesta):
    coincidencias = [ m.start() for m in re.finditer(respuesta, ''.join(frase)) ]
    for inicio in coincidencias: # Para cada ocurrencia de la respuesta (palabra o letra)
        for indice in range(0, len(respuesta)): # Sustituimos los _ por las letras de verdad
            oculta[inicio + indice] = respuesta[indice] 
    return oculta  