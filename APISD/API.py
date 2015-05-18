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
from funciones import *
import pickle

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
    offset = int(offset) #Numero de post a partir del cual empezamos a descargar imagenes, por si nos interesa saltarnos 10 por ejemplo
    peticiones = request.form["peticiones"]
    peticiones  = int(peticiones)
    pedidas = 0
    destino = request.form["destino"] #La carpeta no se crea, DEBE EXISTIR.
    nombre_foto = request.form["nombrefoto"]
    patron = re.compile('(.*\..*\..*\..*)(\..*)') #Nos interesa el grupo 2 (3º) que contendra el formato de la imagen
    while(pedidas < peticiones):
        x = client.posts(user,type=tipo, offset=offset+pedidas)
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
            pedidas = pedidas+1 #Esto cuenta cada post, no cada imagen
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
    
    '''DROPBOX AUTORIZACION'''
    
    
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

    if os.path.exists('./access_token'):
        with open('access_token') as f:
            content = f.read().splitlines()
        dropboxClient = dropbox.client.DropboxClient(content[0])
    else:   
        authorize_url = flow.start()
        print '1. Ir a: ' + authorize_url
        print '2. Click "Permitir"'
        print '3. Copia el codigo de autorizacion.'
        code = raw_input("Introduce el codigo de autorizacion: ").strip()
        access_token, user_id = flow.finish(code)
        #almacenar el token
        f = open('access_token','w')
        f.write(access_token)
        f.close()
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
    patron = re.compile('(.*\..*\..*\..*)(\..*)') #Nos interesa el grupo 2 (3º) que es el que tendra el formato
    while(pedidas < peticiones):
        x = client.posts(user,type=tipo, offset=offset+pedidas)
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

    if os.path.exists('./credentials'):
        fileobject = open('credentials','r')
        credentials = pickle.load(fileobject)
    else:
        # Run through the OAuth flow and retrieve credentials
        flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE,
                           redirect_uri=REDIRECT_URI)
        authorize_url = flow.step1_get_authorize_url()
        print 'Go to the following link in your browser: ' + authorize_url
        code = raw_input('Enter verification code: ').strip()
        credentials = flow.step2_exchange(code)

        #serializar credentials
        credential_stored = 'credentials'
        fileobject = open(credential_stored,'wb')
        pickle.dump(credentials,fileobject)
        fileobject.close()

  
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
    patron = re.compile('(.*\..*\..*\..*)(\..*)') #Nos interesa el grupo 2 (3º) que es el que tendra el formato
    while(pedidas < peticiones):
        x = client.posts(user,type=tipo, offset=offset+pedidas)
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
            pedidas = pedidas+1 #Esto cuenta cada post, no cada imagen
    return render_template('ejecutandose.html')

def d2Drive(downloaded):
        #keys dropbox
    app_key = '160c3ndz3x55jtz'
    app_secret = 'v6ffsipyclu2c3b' 

    #keys drive

    CLIENT_ID = '396600344016-5pu24jntlj54cll8mqpkv02ao3muk2c1.apps.googleusercontent.com'
    CLIENT_SECRET = 'oVIAvf6SAe8ZvF9Ssbngj9sS'
    OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

    #parte dropbox


    with open('access_token') as f:
        content = f.read().splitlines()
    client = dropbox.client.DropboxClient(content[0])
    folder_metadata = client.metadata('/')

    try:
        f, metadata = client.get_file_and_metadata('/'+downloaded)
        out = open(downloaded, 'wb')
        out.write(f.read())
        out.close()
    except dropbox.rest.ErrorResponse:
        print 'el fichero no existe'
        pass

    #parte drive
    # Check https://developers.google.com/drive/scopes for all available scopes
    OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

    # Redirect URI for installed apps
    REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

    # Path to the file to upload
    FILENAME = downloaded

    if os.path.exists('./credentials'):
        fileobject = open('credentials','r')
        credentials = pickle.load(fileobject)
    else:
 # Run through the OAuth flow and retrieve credentials
        flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE,
                               redirect_uri=REDIRECT_URI)
        authorize_url = flow.step1_get_authorize_url()
        print 'Go to the following link in your browser: ' + authorize_url
        code = raw_input('Enter verification code: ').strip()
        credentials = flow.step2_exchange(code)

        #serializar credentials
        credential_stored = 'credentials'
        fileobject = open(credential_stored,'wb')
        pickle.dump(credentials,fileobject)
        fileobject.close()
        #################################

    # Create an httplib2.Http object and authorize it with our credentials
    http = httplib2.Http()
    http = credentials.authorize(http)

    drive_service = build('drive', 'v2', http=http)


    # Insert a file
    media_body = MediaFileUpload(FILENAME, mimetype=metadata['mime_type'], resumable=True)
    body = {
      'title': 'Subido desde dropbox',
      'description': 'Subido desde dropbox',
      'mimeType': metadata['mime_type']
    }

    file = drive_service.files().insert(body=body, media_body=media_body).execute()

    retrieve_all_files(drive_service)
    os.remove(downloaded)




def getdropboxfiles():
    #keys dropbox
    app_key = '160c3ndz3x55jtz'
    app_secret = 'v6ffsipyclu2c3b'
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

    #parte dropbox

    if os.path.exists('./access_token'):
        with open('access_token') as f:
            content = f.read().splitlines()
        client = dropbox.client.DropboxClient(content[0])
    else:
        authorize_url = flow.start()
        print '1. Ir a: ' + authorize_url
        print '2. Click "Permitir"'
        print '3. Copia el codigo de autorizacion.'
        code = raw_input("Introduce el codigo de autorizacion: ").strip()
        access_token, user_id = flow.finish(code)
        #almacenar el token
        f = open('access_token','w')
        f.write(access_token)
        f.close()
        client = dropbox.client.DropboxClient(access_token)

    folder_metadata = client.metadata('/')
    print 'Archivos del directorio'
    print '***********************'

    for files in folder_metadata['contents']:
        f = files['path']
        if files['is_dir']== False:
            print f[1:]

    return folder_metadata['contents']


@app.route("/RecogerValores",  methods=['POST'])
def RecogerValores():
    decision = int(request.form["decision"])
    if(decision == 1):
        return render_template('formulario1.html')
    elif(decision== 2):
        return render_template('formulario2.html')
    elif(decision==3):
        return render_template('formulario3.html')
    else:
        files = getdropboxfiles()
        match = []
        for fi in files:
            f = fi['path']
            if fi['is_dir']== False:
                match.append(f[1:])
        files= match
        return render_template('dropbox_files.html',files=files)

@app.route("/subirDrive",  methods=['POST'])
def subirDrive():
    fichero = request.form['fichero']
    d2Drive(fichero)
    return render_template('ejecutandose.html')

@app.route("/")
def index():
	return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True) # Lanzamos la aplicacion que mostrara el mapa en el navegador.
