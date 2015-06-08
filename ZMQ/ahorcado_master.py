import zmq
# -*- coding: utf-8 -*-

from ahorcado_funciones import *

print "### EL JUEGO DEL AHORCADO ###"
n_jugadores = int(raw_input("Numero de jugadores?: "))

frase = frase_aleatoria()
oculta = ocultar_frase(frase)
acertado = False
turno = 0

print "Servidor activado. Esperando jugadores..."
sockets = generar_sockets(n_jugadores)
puertos_asignados = asignar_puertos(n_jugadores)

# Conectamos con los jugadores
for i in range(0, n_jugadores):
    sockets[i].connect("tcp://localhost:"+str(puertos_asignados[i]))


# Comienza el juego
print "FRASE A ADIVINAR: ", frase
while acertado == False:
    sockets[turno].send(lista_a_cadena(oculta))
    respuesta = sockets[turno].recv()

    oculta = actualizar_frase_oculta(oculta, frase, respuesta)
    print "Jugador ", turno, ": ", lista_a_cadena(oculta)
    
    sockets[turno].send(lista_a_cadena(oculta))
    
    sockets[turno].recv()

    if lista_a_cadena(oculta).find('_') == -1:
        acertado = True
        print "El jugador ", turno, " ha ganado."
        for jugador in range(0, n_jugadores):
            if jugador != turno: # Se notifica al resto de los jugadores que han perdido.
                sockets[jugador].send("-1") # Código que indica que alguien ha ganado.
        
    turno = (turno+1) % n_jugadores







