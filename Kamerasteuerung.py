import os, pickle           # Hier werden einzelne Module importiert,
from RPi import GPIO        # sie werden für das Programm später benötigt.
from time import sleep      # Dazu gehören vor allem die GPIO-Schnittstellen
GPIO.setwarnings(False)     # des Raspberry Pi’s, die daraufhin eingestellt werden.
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

def blinken(zeit):              # Die Funktion „blinken“ lässt die LEDs an der Kamera
    t = zeit                    # nach einer Zeitangabe in jeweils einer Sekunde
    while not t <= 0:           # aufleuchten und wieder ausgehen. Dies ist praktisch,
        GPIO.output(12, True)   # um zu erkennen, ob bald ein Foto gemacht wird.
        sleep(0.5)
        GPIO.output(12, False)
        sleep(0.5)
        t -= 1

def schiesseFoto(breite,hoehe,bildname,verzeichnis):            # Dort wird das Foto als png-file mit einer
    befehl = "python read-sensors.py > Messwerte_Aktuell.txt"   # angegebenen Größen in einem angegeben Verzeichnis
    os.system(befehl)                                           # geschossen und die Messwerte des Sensor-Moduls
    with open('Messwerte_Aktuell.txt') as f:                    # werden in einer Datei abgespeichert.
        data = f.readline()[:-1]                                # Die Messwerte sind zudem auch auf den Bildern
    if os.path.exists(verzeichnis+"Messwerte.dat"):             # als Text darüber geschrieben.
        h = open(verzeichnis+"Messwerte.dat","rb")
        messwerte = pickle.load(h)
        h.close()
        messwerte.append(data)
        messwerteneu = messwerte[:]
        g = open(verzeichnis+"Messwerte.dat","wb")
        pickle.dump(messwerteneu,g)
        g.close()
    else:
        messwerteneu = []
        messwerteneu.append(data)
        g = open(verzeichnis+"Messwerte.dat","wb")
        pickle.dump(messwerteneu,g)
        g.close()
    GPIO.output(12, True)
    befehl = "raspistill -ae 20,0x00 -a '%s' -w %i -h %i -e png -t 300 -o %s -n" % (data,breite,hoehe,bildname)
    os.system(befehl)
    sleep(0.5)
    GPIO.output(12, False)
