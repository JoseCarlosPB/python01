# Trabajo sobre ZMQ donde hemos implementado el juego del ahorcado 
# El archivo ahorcado master es el servidor, el que controla el juego y el numero de jugadores que se aceptaran en la partida
# Posteriormente cada vez que se ejecute el ahorcado_player se le asignará un puerto y será un jugador de la partida, los jugadores deberan # esperar a que esten 
# Todos los jugadores que conformarán la partida conectados

# El juego del ahorcado consiste en un juego donde el servidor te propone una frase oculta, y cada jugador debe ir probando alguna letra, # palabra o frase a ver si está
# Si fallan muchas veces diciendo cosas que no estan incluidas en la frase a adivinar, el juego se pierde. si adivinan la frase entera ganan.
# Cada jugador en su turno podrá decir una letra frase o palabra y el servidor si se encuentra en la frase a adivinar, desvelará donde se # encuentra. 
