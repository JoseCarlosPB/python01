import twitter
import json
from flask import Flask, render_template
from flask.ext.googlemaps import GoogleMaps
from flask.ext.googlemaps import Map

app = Flask(__name__)
GoogleMaps(app)

CONSUMER_KEY = 'W1MLNTl9NG0WTDYxzwsnu6vY8'
CONSUMER_SECRET = 'cLI16odQnEiFQowFLrd49hLJxpuHLiEc7LJE2P3cln56NGqgc0'
OAUTH_TOKEN = '406594742-bnsr9bIfThPRpyia1GsIQBQ2e4AxAjQf6uAEfBrc'
OAUTH_TOKEN_SECRET = 'B8OBY9ZT8li1NKhskOyr4xufWgcvnF0UffZ4OnCw7XJF6'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth) # Obtenemos la API de Twitter tras autentificarnos. 

q = 'hello'
cantidad= 100 # Cantidad de tweets que queremos.

resultados = twitter_api.search.tweets(q=q, count=cantidad)


coords= [] # Lista que contendra las coordenadas

for elto in resultados["statuses"]:
    if elto["coordinates"] is not None: # Si es none, es que las coordenadas que se encuentran en "geo" no estan disponibles.
        tupla= (elto["geo"]["coordinates"][0] , elto["geo"]["coordinates"][1])
        coords.append(tupla)
        

# Establecemos la configuracion del mapa resultante.
@app.route("/")
def mapview():
    mymap = Map(
        identifier="mapa-resultante",
        lat=40.3450396,
        lng=-3.6517684,
        markers= coords, # Asignamos las coordenadas que se marcaran en el mapa.
        style="height:800px;width:800px;margin:0;",
		zoom= 4
    ) 
    return render_template('template2.html', mymap=mymap)

if __name__ == "__main__":
    app.run(debug=True) # Lanzamos la aplicacion que mostrara el mapa en el navegador.