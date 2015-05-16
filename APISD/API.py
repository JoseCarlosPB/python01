# -*- coding: utf-8 -*-
import pytumblr
import dropbox
import os #join es mas rapido que concatenar cadenas 
import re
import urllib
import httplib2
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from flask import Flask, render_template
from flask import request

app = Flask(__name__)

@app.route("/tumblr",methods=['POST'])
def tumblr():
    client = pytumblr.TumblrRestClient(
    'jIfKda0a2sHShUJtwfJt8fA7nYv0bzU2reXEq4sOCgRWWe7XJH',
    'D8nPNtDzT69Yrfa63X82PjfRBmc72140rlBgTBWtJMpWb3b2w5',
    'oc7bgJkAFj7dP4LwRHagPPhJpI48OyXx0D51IAfqFqLd9LSQyi',
    'QdwKNqJkZYdZP94KrCRnXFRyUQXZjgzt0buskgv01nUGvjxFSd',
    )
    index = 0
    user = request.form["user"]
    tipo = 'photo'
    offset = request.form["offset"]
    offset = int(offset)
    peticiones = request.form["peticiones"]
    peticiones  = int(peticiones)
    pedidas = 0
    destino = request.form["destino"] #La carpeta no se crea, DEBE EXISTIR.
    nombre_foto = request.form["nombrefoto"]
    patron = re.compile('(.*\..*\..*\..*)(\..*)') #Nos interesa el grupo 2 (3º)
    while(pedidas < peticiones):
        x = client.posts(user,type=tipo, offset=offset+pedidas, tag = "")
        #ese grupo tendra el .formato 
        for lista in x['posts']:
            if pedidas<peticiones:
                for fotos in lista['photos']:
                    url = fotos['original_size']['url']
                    matcher = patron.search(url)
                    formato = matcher.group(2)
                    destinonombre = os.path.join(destino,nombre_foto+str(index)+formato)
                    #el path join hace que a imagenes le ponga al final otro /y concatene con el nombre del fichero
                    urllib.urlretrieve(url, destinonombre)
                    index= index+1
            pedidas = pedidas+1 #Esto cuenta cada post, no cada imgen
    return render_template('ejecutandose.html')
@app.route("/tumblr2dropbox", methods=['POST'])
def tumbl2dropbox():
    ''' KEYS TUMBLR '''
    client = pytumblr.TumblrRestClient(
    'jIfKda0a2sHShUJtwfJt8fA7nYv0bzU2reXEq4sOCgRWWe7XJH',
    'D8nPNtDzT69Yrfa63X82PjfRBmc72140rlBgTBWtJMpWb3b2w5',
    'oc7bgJkAFj7dP4LwRHagPPhJpI48OyXx0D51IAfqFqLd9LSQyi',
    'QdwKNqJkZYdZP94KrCRnXFRyUQXZjgzt0buskgv01nUGvjxFSd',
    )

    ''' KEYS DROPBOX '''
    app_key = '160c3ndz3x55jtz'
    app_secret = 'v6ffsipyclu2c3b'
    #access_token = 'bxp6d2gqlTAAAAAAAAAAonls1U_b30H18p3EStSQ2ech4fcM5wD_qEb6ttFXblif'
    
    
    
    '''DROPBOX AUTORIZACION'''
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
    authorize_url = flow.start()
    print '1. Go to: ' + authorize_url
    print '2. Click "Allow" (you might have to log in first)'
    print '3. Copy the authorization code.'
    code = raw_input("Enter the authorization code here: ").strip()
    access_token, user_id = flow.finish(code)
    
    dropboxClient = dropbox.client.DropboxClient(access_token)
    ''' TUMBLR '''
    index = 0
    user = request.form["user"]
    tipo = 'photo'
    offset = request.form["offset"]
    offset = int(offset)
    peticiones = request.form["peticiones"]
    peticiones  = int(peticiones)
    pedidas = 0
    destino = request.form["destino"] #La carpeta no se crea, DEBE EXISTIR.
    destinoDropbox = request.form["destinodropbox"]
    nombre_foto = request.form["nombrefoto"]
    patron = re.compile('(.*\..*\..*\..*)(\..*)') #Nos interesa el grupo 2 (3º)
    while(pedidas < peticiones):
        x = client.posts(user,type=tipo, offset=offset+pedidas, tag = "")
        #ese grupo tendra el .formato 
        for lista in x['posts']:
            if pedidas<peticiones:
                for fotos in lista['photos']:
                    url = fotos['original_size']['url']
                    matcher = patron.search(url)
                    formato = matcher.group(2)
                    destinonombre = os.path.join(destino,nombre_foto+str(index)+formato)
                    #el path join hace que a imagenes le ponga al final otro /y concatene con el nombre del fichero
                    urllib.urlretrieve(url, destinonombre)
                    file = open(destinonombre) #abrimos la imagen como objeto 
                    #Aqui ya hemos descargado la imagen, ahora a subirla a dropbox
                    destinoDropboxURL = os.path.join(destinoDropbox,nombre_foto+str(index)+formato)
                    response = dropboxClient.put_file(destinoDropboxURL,file, overwrite = False)#f = false, no sobreescritura
                    index= index+1
            pedidas = pedidas+1 #Esto cuenta cada post, no cada imgen
    return render_template('ejecutandose.html')    
@app.route("/tumblr2drive", methods=['POST'])
def tumblr2drive():
    ''' KEYS TUMBLR '''
    client = pytumblr.TumblrRestClient(
    'jIfKda0a2sHShUJtwfJt8fA7nYv0bzU2reXEq4sOCgRWWe7XJH',
    'D8nPNtDzT69Yrfa63X82PjfRBmc72140rlBgTBWtJMpWb3b2w5',
    'oc7bgJkAFj7dP4LwRHagPPhJpI48OyXx0D51IAfqFqLd9LSQyi',
    'QdwKNqJkZYdZP94KrCRnXFRyUQXZjgzt0buskgv01nUGvjxFSd',
    )
    
    CLIENT_ID = '396600344016-5pu24jntlj54cll8mqpkv02ao3muk2c1.apps.googleusercontent.com'
    CLIENT_SECRET = 'oVIAvf6SAe8ZvF9Ssbngj9sS'
    OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

    # Redirect URI for installed apps
    REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

    # Run through the OAuth flow and retrieve credentials
    flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE,
                           redirect_uri=REDIRECT_URI)
    authorize_url = flow.step1_get_authorize_url()

    print 'Go to the following link in your browser: ' + authorize_url
    code = raw_input('Enter verification code: ').strip()
    credentials = flow.step2_exchange(code)

    # Create an httplib2.Http object and authorize it with our credentials
    http = httplib2.Http()
    http = credentials.authorize(http)

    mimetype = 'image/jpg'

    drive_service = build('drive', 'v2', http=http)

    index = 0
    user = request.form["user"]
    tipo = 'photo'
    offset = request.form["offset"]
    offset = int(offset)
    peticiones = request.form["peticiones"]
    peticiones  = int(peticiones)
    pedidas = 0
    destino = request.form["destino"] #La carpeta no se crea, DEBE EXISTIR.
    nombre_foto = request.form["nombrefoto"]
    patron = re.compile('(.*\..*\..*\..*)(\..*)') #Nos interesa el grupo 2 (3º)
    while(pedidas < peticiones):
        x = client.posts(user,type=tipo, offset=offset+pedidas, tag = "")
        #ese grupo tendra el .formato 
        for lista in x['posts']:
            if pedidas<peticiones:
                for fotos in lista['photos']:
                    url = fotos['original_size']['url']
                    matcher = patron.search(url)
                    formato = matcher.group(2)
                    destinonombre = os.path.join(destino,nombre_foto+str(index)+formato)
                    #el path join hace que a imagenes le ponga al final otro /y concatene con el nombre del fichero
                    urllib.urlretrieve(url, destinonombre)
                    media_body = MediaFileUpload(destinonombre, mimetype=mimetype, resumable=True)
                    body = {
                    'title': nombre_foto+str(index),
                    'description': 'Foto subida desde la aplicación API de SD.',
                    'mimeType': mimetype
                    }

                    drive_service.files().insert(body=body, media_body=media_body).execute()
                    index= index+1
            pedidas = pedidas+1 #Esto cuenta cada post, no cada imgen
    return render_template('ejecutandose.html')

@app.route("/RecogerValores",  methods=['POST'])
def RecogerValores():
    decision = int(request.form["decision"])
    if(decision == 1):
        print "hola desde 1"
        return render_template('formulario1.html')
    elif(decision== 2):
        print "hola desde 2"
        return render_template('formulario2.html')
    else:
        print "hola desde 3"
        return render_template('formulario3.html')
    

@app.route("/")
def index():
	return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True) # Lanzamos la aplicacion que mostrara el mapa en el navegador.
