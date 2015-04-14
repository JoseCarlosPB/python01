import twitter
import json
from flask import Flask, render_template
from flask.ext.googlemaps import GoogleMaps
from flask.ext.googlemaps import Map
from flask import request

app = Flask(__name__)
GoogleMaps(app)

CONSUMER_KEY = 'W1MLNTl9NG0WTDYxzwsnu6vY8'
CONSUMER_SECRET = 'cLI16odQnEiFQowFLrd49hLJxpuHLiEc7LJE2P3cln56NGqgc0'
OAUTH_TOKEN = '406594742-bnsr9bIfThPRpyia1GsIQBQ2e4AxAjQf6uAEfBrc'
OAUTH_TOKEN_SECRET = 'B8OBY9ZT8li1NKhskOyr4xufWgcvnF0UffZ4OnCw7XJF6'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth) # Obtenemos la API de Twitter tras autentificarnos. 

cantidad= 100 # Cantidad de tweets que queremos.
geo = "40.2085,-3.713,497mi"

coords= [] # Lista que contendra las coordenadas

@app.route("/buscar", methods=['POST'])
def buscar():
    termino = request.form['text'] 
    resultados = twitter_api.search.tweets(q=termino, count=cantidad, geocode = geo)
    for elto in resultados["statuses"]:
        if elto["coordinates"] is not None: 
            tupla= (elto["geo"]["coordinates"][0] , elto["geo"]["coordinates"][1])
            coords.append(tupla)
    mymap = Map(
	     identifier="view-side",
		  lat=40.3450396,
		  lng=-3.6517684,
		  zoom=6,
		  markers=coords,
		  style="height:800px;width:800px;margin:0;"
	 ) 
    return render_template('mapa.html', mymap=mymap)

@app.route("/")
def index():
	return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True) # Lanzamos la aplicacion que mostrara el mapa en el navegador.
