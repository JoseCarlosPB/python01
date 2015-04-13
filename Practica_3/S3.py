import twitter
import json
from flask import Flask, render_template
from flask.ext.googlemaps import GoogleMaps
from flask.ext.googlemaps import Map

app = Flask(__name__)
GoogleMaps(app)

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

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