import os
import zipfile
import requests


# So kann man eine Zip-Datei aus dem Internet laden:
url_pyenguin = "https://github.com/coderdojoka/pyenguin/archive/master.zip"
response = requests.get(url_pyenguin)

# Datei herunterladen Kann eine Weile dauern!!
zipDaten = response.content

# Daten als eine Binär-Datei speichern
datei = open("pyenguin_download.zip", "wb")
datei.write(zipDaten)
datei.close()


# Eine Zip-Datei entpacken. TODO: Pfad anpassen!
zip_ref = zipfile.ZipFile("meine_datei.zip")
# Alles im aktuellen Verzeichnis entpacken
zip_ref.extractall("")
zip_ref.close()


# os.system führt einen Befehl in der Konsole aus
# Der Pfad muss auf die heruntergeladene und entpackte setup.py Datei sein
# TODO: pfad anpassen
#os.system("python pfad/zu/setup.py install")
