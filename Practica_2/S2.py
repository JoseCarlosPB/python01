
fichero= open("texto.txt", "r");
palabras= fichero.read() 
palabras= palabras.split(" ")

# La solución se va guardando en la lista "encadenadas".
def palabrasEncadRec(palabras, actual, encadenadas):
    for palabra in palabras:
        # Miramos que la palabra no haya sido considerada aún, o podríamos caer en
        # bucles infinitos.
        if palabra not in encadenadas and actual[len(actual)-1]==palabra[0]:
            encadenadas.append(palabra)
            palabrasEncadRec(palabras, palabra, encadenadas)
    

mejorSolucion= []
for actual in palabras:
    encadenadas= [actual]
    # Este bucle va viendo cuántas palabras puede encadenar si empieza por "actual".
    palabrasEncadRec(palabras, actual, encadenadas)
    if len(encadenadas) > len(mejorSolucion):
        # La cadena más larga es la que se guarda como mejor solución.
        mejorSolucion= encadenadas
print 'La mejor solucion es: ', mejorSolucion