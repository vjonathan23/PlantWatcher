# Import von benötigten Modulen
import os               # Befehle auf Betriebssystemebene
import pickle           # Zugriff auf Binär-Dateien
from RPi import GPIO    # Zugriff auf GPIO Pins des Raspberry Pi 
from time import sleep  # Zeitdelay für LED-Ring (blinken)

# GPIO Initialisierung
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)    # Von Pin 12 aus wird der LED-Ring angesteuert

# Die Funktion *blinken* lässt den LED-Ring an der Kamera
# über einen Zeitraum in Sekunden in jeweils einer Sekunde
# aufleuchten und wieder ausgehen. Dies ist praktisch,
# um zu erkennen, ob bald ein Foto gemacht wird.
def blinken(zeit):              
    t = zeit                    
    while not t <= 0:           
        GPIO.output(12, True)   
        sleep(0.5)              
        GPIO.output(12, False)
        sleep(0.5)
        t -= 1

# In der Funktion *schiesseFoto* wird das Foto als png-File *bildname* mit einer
# angegebenen Größen *breite/hoehe* in einem angegeben Verzeichnis *verzeichnis*
# erstellt und die Messwerte des Sensor-Moduls werden in einer Datei abgespeichert.
# Die Messwerte sind zudem auch auf den Bildern als Text darüber geschrieben.
def schiesseFoto(breite,hoehe,bildname,verzeichnis):
    # Sensordaten in eine temporäre Datei speichern
    befehl = "python read-sensors.py > Messwerte_Aktuell.txt"   
    os.system(befehl)
    # Einlesen der temporären Datei mit den ermittelten Sensorwerten in die Variable *data*
    with open('Messwerte_Aktuell.txt') as f:                    
        data = f.readline()[:-1]
    # Daten in zentrale Sammeldatei fortschreiben
    if os.path.exists(verzeichnis+"Messwerte.dat"):             
        # Vorhandene Messwert-Sammeldatei öffnen
        h = open(verzeichnis+"Messwerte.dat","rb")
        messwerte = pickle.load(h)
        h.close()
    else:
        # Neue Datei erstellen
        messwerte = []
    messwerte.append(data)
    messwerteneu = messwerte[:] # Kopie erstellen

    # Messwerte in zentrale Datei speichern 
    g = open(verzeichnis+"Messwerte.dat","wb")
    pickle.dump(messwerteneu,g)
    g.close()
    
    # LED-Ring einschalten
    GPIO.output(12, True)
    # Foto aufnehmen und Messwerte ins Bild übernehmen
    # Parameter von *raspistill*
    #   -ae Textgröße + Farbe des einzublendenden Texts
    #   -a  Einzublendender Text (string *data*)
    #   -w  Breite (integer *breite*)
    #   -h  Höhe (integer *hoehe*)
    #   -e  Dateiformart
    #   -t  Zeitverzörgerung in Millisekunden (notwendig, da sonst Fehler auftreten)
    #   -o  Ausgabedatei inkl. Verzeichnis (string *bildname*)
    #   -n  Kein Preview
    # siehe auch: https://www.raspberrypi.org/documentation/raspbian/applications/camera.md
    befehl = "raspistill -ae 20,0x00 -a '%s' -w %i -h %i -e png -t 300 -o %s -n" % (data,breite,hoehe,bildname)
    os.system(befehl)
    # LED-Ring ausschalten
    sleep(0.5)
    GPIO.output(12, False)
