# Hier werden einzelne Module importiert, sie werden für das Programm später benötigt.
from Kamerasteuerung import schiesseFoto, blinken   # Eigenes Modul für Kamerasteuerung
from tkinter import *                               # GUI (Graphische Benutzeroberfläche)
from time import *                                  # Zeitmessung
import _thread                                      # Paralleler Start von 2 Funktionen
import os                                           # Befehle auf Betriebssystemebene
import pickle                                       # Zugriff auf Binär-Dateien
import matplotlib.pyplot as plt                     # PyPlot zur Ausgabe des Messwert-Diagramms

# Globale Variablen
einheiten = ["s","min","h","d"]                     # Zeiteinheiten für das Zeit-Intervall                    
faktoren = [1,60,3600,86400]                        # Umrechnungsfaktoren für Zeit-Intervalle nach Sekunden
start = False                                       # Boolean-Variable für Start/Stop-Funktion
startZeit = 0                                       # Zeitstempel für den Startpunkt der Messung
zeit = 0                                            # Vergangene Zeit seit dem Start in Sekunden

# Dialog zur Verzeichnis-Auswahl für den Projektordner
def Verzeichniswaehlen():
    v = filedialog.askdirectory()
    if v:
        textVerzeichnis.delete(1.0,END)
        textVerzeichnis.insert(1.0,v+"/")

# Die Funktion *check* dient zur Kontrolle, ob das gewählte Verzeichnis überhaupt existiert.
# Falls dieses nämlich nicht existiert, besteht die Möglichkeit dieses direkt zu erzeugen.
def check():                                                        
    v = textVerzeichnis.get(1.0,END)[:-1]                           
    if os.path.isdir(v):                                            
        messagebox.showinfo(message="Dieses Verzeichnis existiert") 
    else:
        if messagebox.askyesno(message="Dieses Verzeichnis existiert nicht. Wollen sie dieses Verzeichnis erzeugen?"):
            os.makedirs(v)  # Anlegen eines neuen Verzeichnis
        else:
            messagebox.showinfo(message="Bitte ändern sie das Verzeichnis")
    
# Mit der Funktion *Start* wird ein Projekt gestartet oder gestoppt.
def Start():
    global start, startZeit
    if start == False:
        startZeit = time()      # Setzen der Startzeit
        start = True
    else:
        start = False

# Hier wird mithilfe der Funktion *Interval* die Einstellung des Intervalls vorgenommen.
# Das erste Element der Liste *einheiten* ist die aktuell ausgewählte Einheit.
# Die Funktion rotiert die Liste um 1 Element
def Interval():                         
    global einheiten,faktoren           
    ersteEinheit = einheiten.pop(0)
    ersterFaktor = faktoren.pop(0)
    einheiten.append(ersteEinheit)
    faktoren.append(ersterFaktor)
    # Einstellen der neuen aktiven Einheit auf der GUI
    buttonInterval.config(text=einheiten[0])

# In der Funktion *Bilder* wird die Bilderstellung nach Intervall gesteuert.
# Die Bilder werden nach Zeitpunkt abgespeichert, auf der Benutzeroberfläche angezeigt und die Anzahl der Bilder wird erhöht.
# Diese Funktion läuft über einen Thread, das bedeutet, dass die Funktion neben dem eigentlichen Programm weiterlaufen kann.
def Bilder():
    global zeit
    letzteZeit = 0
    bildAnzahl = 0
    while True:
        zeitInt = int(zeit)
        if start:
            faktor = faktoren[0]
            interval = textInterval.get(1.0,END)[:-1]
            interval = float(interval) * faktor
            verzeichnis = textVerzeichnis.get(1.0,END)[:-1]
            if os.path.isdir(verzeichnis):
                if zeitInt - (letzteZeit) + int(interval/10) >= interval:
                    # Foto durch Blink-Signal einleiten
                    blinken(int(interval/10))
                    # Datum und Uhrzeit für Dateinamen aufbereiten (Zur Sortierung muss zuerst das Jahr, dann der Monat und dann der Tag als Dateiname verwendet werden)
                    timedata = [str(localtime().tm_year),str(localtime().tm_mon),str(localtime().tm_mday),str(localtime().tm_hour),str(localtime().tm_min),str(localtime().tm_sec)]
                    for c in range(len(timedata)):
                        if len(timedata[0]) < 2:
                            g = "0"+timedata[0] # z.B. Monats-Tag 5 -> 05 umwandeln 
                        else:
                            g = timedata[0]
                        del timedata[0]
                        timedata.append(g)
                    BildZeit = "".join(timedata)  # Zeit-String zusammenfügen aus den einzelnen Elementen
                    # Foto erstellen
                    schiesseFoto(400,300,verzeichnis+"img_"+BildZeit+".png",verzeichnis)
                    # Letzte Zeit merken
                    letzteZeit = zeitInt + int(interval/10)
                    # GUI aktualisieren
                    labelDatum.config(text=asctime())
                    letztesBild = PhotoImage(master=window,file=verzeichnis+"img_"+BildZeit+".png")
                    letztesBild = letztesBild.subsample(2)
                    labelLetztesBild.config(image=letztesBild)
                    bildAnzahl += 1
                    labelAnzahlBilder.config(text="Anzahl der Bilder: "+str(bildAnzahl))
            else:
                messagebox.showerror(message="Das Verzeichnis existiert nicht!")
        else:
            # GUI bei Stopp zurücksetzen
            bildAnzahl = 0
            letzteZeit = 0
            labelAnzahlBilder.config(text="Anzahl der Bilder: "+str(bildAnzahl))    
        sleep(0.01)

# Auch die Funktion *Zeitanpassung* wird über einen Thread angesteuert.
# Sie bewirkt, dass die vergangene Zeit des Timers richtig
# auf den dafür vorgesehenen GUI-Bereich angezeigt wird und
# dass die Zeit vor allem für die Funktion *Bilder*,
# die die vergangene Zeit zur Berechnung, wann ein Bild
# gemacht werden soll, benötigt, zur Verfügung steht.
def Zeitanpassung():
    global zeit
    while True:
        if start:
            zeit = time() - startZeit
            zeit = round(zeit,4)
            zeitInt = int(zeit)
            if zeitInt < 60:
                if zeitInt < 10:
                    labelZeit.config(text="Zeit: 0:00:0"+str(zeitInt))
                else:
                    labelZeit.config(text="Zeit: 0:00:"+str(zeitInt))
            elif zeitInt < 3600:
                zeitMinRest = zeitInt % 60
                zeitMin = (zeitInt - zeitMinRest) / 60
                zeitS = zeitMinRest
                zeitMin = int(zeitMin)
                zeitS = int(zeitS)
                if zeitS < 10 and zeitMin < 10:
                    labelZeit.config(text="Zeit: 0:0"+str(zeitMin)+":0"+str(zeitS))
                elif zeitS < 10:
                    labelZeit.config(text="Zeit: 0:"+str(zeitMin)+":0"+str(zeitS))
                elif zeitMin < 10:
                    labelZeit.config(text="Zeit: 0:0"+str(zeitMin)+":"+str(zeitS))
                else:
                    labelZeit.config(text="Zeit: 0:"+str(zeitMin)+":"+str(zeitS))
            else:
                zeitHRest = zeitInt % 3600
                zeitH = (zeitInt - zeitHRest) / 3600
                zeitMinRest = zeitHRest % 60
                zeitMin = (zeitHRest - zeitMinRest) / 60
                zeitS =  zeitMinRest
                zeitH = int(zeitH)
                zeitMin = int(zeitMin)
                zeitS = int(zeitS)
                if zeitS < 10 and zeitMin < 10:
                    labelZeit.config(text="Zeit: "+str(zeitH)+":0"+str(zeitMin)+":0"+str(zeitS))
                elif zeitS < 10:
                    labelZeit.config(text="Zeit: "+str(zeitH)+":"+str(zeitMin)+":0"+str(zeitS))
                elif zeitMin < 10:
                    labelZeit.config(text="Zeit: "+str(zeitH)+":0"+str(zeitMin)+":"+str(zeitS))
                else:
                    labelZeit.config(text="Zeit: "+str(zeitH)+":"+str(zeitMin)+":"+str(zeitS))
        else:
            zeit = 0
        sleep(0.01)

# Die Funktion *Video* erstellt eine Animation des Pflanzenwachstums durch die Bilder.
# Hier wird das Programm *feh* verwendetet. Hier muss eine Anzahl von FPS (frames per second)
# und das Verzeichnis mit angegeben werden.
def Video():
    # FPS uns Verzeichniseingabe vom GUI holen
    fps = float(textFps.get(1.0,END)[:-1])
    verzeichnis = textVerzeichnis.get(1.0,END)[:-1]
    # *feh* im Vollbildmodus starten
    # Verwendete Parameter:
    #   -Y  Mauszeiger verstecken
    #   -x  rahmenloses Fenster
    #   -q  quiet mode (keine Fehler anzeigen)
    #   -D  Delay in Sekunden für Diashow
    #   -B  Hintergrundfarbe
    #   -F  Fullscreen
    #   -Z  Auto-Zoom der Bilder
    #   -d  Dateiname im Bild mit anzeigen (um Datum/Uhrzeit zu erkennen)
    if os.path.isdir(verzeichnis):
        command = "feh -Y -x -q -D "+str(1/fps)+" -B black -F -Z -d "+verzeichnis+"*"
        os.system(command)
    else:
        messagebox.showerror(message="Das Verzeichnis existiert nicht!")

# Mithilfe von der Funktion *Messwerte* können die Messdaten des Sensor-Moduls,
# welche in einer Datei abgespeichert sind, gelesen werden. Diese werden dann so geordnet,
# dass mit dem Programm *Pyplot* Graphen aus den Messwerten erstellt werden können.
# Hierzu ist auch das Intervall wichtig, um die richtigen Zeitabstände in den Graphen
# wiederzugeben. Auch ein Durchschnittsmesswert wird für die jeweilige Kategorie mitgegeben.
def Messwerte():
    einheit = einheiten[0]
    interval = int(textInterval.get(1.0,END)[:-1])
    verzeichnis = textVerzeichnis.get(1.0,END)[:-1]
    if os.path.exists(verzeichnis+"Messwerte.dat"):
        h = open(verzeichnis+"Messwerte.dat","rb")
        messwerte = pickle.load(h)
        h.close()
        # x-Achse erstellen
        x = []
        for i in range(1,len(messwerte)+1):
            x.append(i*interval)
        # Erstelle Liste mit Messwerten ohne Einheit
        messwerteneu = []
        for g in messwerte:
            h = g
            h = h.split(' C ')
            messwerteneu.append(float(h[0]))
            del h[0]
            h = h[0]
            h = h.split(' hPa ')
            messwerteneu.append(float(h[0]))
            del h[0]
            h = h[0]
            h = h.split(' %RL')
            messwerteneu.append(float(h[0]))
            del h[0]
            h = h[0]
        # y-Achse mit 3 Kurven aufbauen
        yT = []
        yLf = []
        yLd = []
        w = 0
        for i in messwerteneu:
            if w % 3 == 0:
                yT.append(i)
            elif w % 3 == 1:
                yLd.append(i)
            elif w % 3 == 2:
                yLf.append(i)
            w += 1
        # Durchschnittswerte bestimmen
        yTD = 0
        for i in yT:
            yTD = yTD + i
        yTD = yTD / len(yT)
        yLfD = 0
        for i in yLf:
            yLfD = yLfD + i
        yLfD = yLfD / len(yLf)
        yLdD = 0
        for i in yLd:
            yLdD = yLdD + i
        yLdD = yLdD / len(yLd)

        # Plot erstellen
        fig,p = plt.subplots(3, 1,num='JuFo')
        # Messreihe 1: Temperatur
        p[0].plot(x,yT,'ro-')
        p[0].set_title('Temperatur (Ø %.2f °C)' % yTD)
        p[0].set_ylabel('°C')
        # Messreihe 2: Luftdruck
        p[1].plot(x,yLd,'go-')
        p[1].set_title('Luftdruck (Ø %.2f hPa)' % yLdD)
        p[1].set_ylabel('hPa')
        # Messreihe 3: Luftfeuchtigkeit
        p[2].plot(x,yLf,'bo-')
        p[2].set_title('Luftfeuchtigkeit (Ø %.2f% %)' % yLfD)
        p[2].set_ylabel('%')
        # x-Achse
        p[2].set_xlabel('Zeit ('+einheit+')')
        # Layout: Abstand zwischen den Graphen
        plt.tight_layout(pad=0.4,w_pad=0.5,h_pad=1.0)
        # Diagramme ausgeben
        plt.show()
    else:
        messagebox.showerror(message="Die Messwerte.dat-Datei existiert nicht!")

# Diese letzte Funktion ist die Hauptfunktion, hier werden alle anderen Funktionen in einer
# graphischen Benutzeroberfläche mithilfe von dem Python-Modul *tkinter* bereitgestellt.
# Einzelne Buttons, Labels und Textfelder werden hier erstellt und den Funktionen
# zugewiesen, welche dann Interaktionen hervorrufen. Diese GUI-Elemente werden
# in einem Gitter-Layout (Grid) angeordnet.
def Hauptprogramm():
    global window,labelAnzahlBilder,buttonInterval,labelZeit,letztesBild,labelLetztesBild,labelDatum,textInterval,textVerzeichnis,textFps
    # Tkinter Fenster erstellen
    window = Tk()
    window.title("Das Geheimnis des Wachstums")
    # Elemente platzieren
    letztesBild = None
    labelLetztesBild = Label(master=window,font=("Arial",14),
                             text="Keine Bilder")
    labelLetztesBild.grid(column=2,row=0,columnspan=10,rowspan=11)
    labelDatum = Label(master=window,font=("Arial",14))
    labelDatum.grid(column=2,row=11,columnspan=10)
    labelVerzeichnis = Label(master=window,font=("Arial",14),
                             text="Verzeichnis")
    labelVerzeichnis.grid(column=0,row=1,sticky=W)
    labelInterval = Label(master=window,font=("Arial",14),
                          text="Intervall")
    labelInterval.grid(column=0,row=4,sticky=W)
    labelZeit = Label(master=window,font=("Arial",14),
                      text="Zeit: 0:00:00")
    labelZeit.grid(column=0,row=6,sticky=W)
    labelAnzahlBilder = Label(master=window,font=("Arial",14),
                              text="Anzahl der Bilder: 0")
    labelAnzahlBilder.grid(column=0,row=7,sticky=W)
    labelFps = Label(master=window,font=("Arial",14),
                     text="FPS")
    labelFps.grid(column=1,row=9,sticky=W)
    labelVideo = Label(master=window,font=("Arial",14),
                       text="Video-Optionen")
    labelVideo.grid(column=0,row=8,columnspan=2,sticky=W)
    buttonStartStop = Button(master=window,text="Start / Stop",width=22,
                             font=("Arial",14),command=Start)
    buttonStartStop.grid(column=0,row=0,columnspan=2,sticky=W)
    buttonInterval = Button(master=window,text="s",width=5,
                            font=("Arial",14),command=Interval)
    buttonInterval.grid(column=1,row=5,sticky=W)
    buttonVideo = Button(master=window,text="Video ansehen",width=22,
                         font=("Arial",14),command=Video)
    buttonVideo.grid(column=0,row=10,columnspan=2,sticky=W)
    buttonVerzeichnis = Button(master=window,text="Wähle Verzeichnis",width=14,
                         font=("Arial",14),command=Verzeichniswaehlen)
    buttonVerzeichnis.grid(column=0,row=2,sticky=W)
    buttonPruefeExistenz = Button(master=window,text="Prüfe",width=5,
                         font=("Arial",14),command=check)
    buttonPruefeExistenz.grid(column=1,row=2,sticky=W)
    buttonMesstabelle = Button(master=window,text="Erstelle Messwertdiagramm",
                               width=22,font=("Arial",14),command=Messwerte)
    buttonMesstabelle.grid(column=0,row=11,columnspan=2,sticky=W)
    textVerzeichnis = Text(master=window,font=("Arial",14),width=24,
                           height=1)
    textVerzeichnis.grid(column=0,row=3,sticky=W,columnspan=2)
    textVerzeichnis.insert(END,"/home/pi/Programme/Jufo-ProjektWachstum/")
    textInterval = Text(master=window,font=("Arial",14),width=12,
                        height=1)
    textInterval.grid(column=0,row=5,sticky=W)
    textFps = Text(master=window,font=("Arial",14),width=12,
                           height=1)
    textFps.grid(column=0,row=9,sticky=W)
    # Thread für Zeitmessung starten
    _thread.start_new_thread(Zeitanpassung,())
    # Thread für Bildaufnahme starten
    _thread.start_new_thread(Bilder,())
    # Fenster starten
    window.mainloop()

# Hauptprogramm starten
Hauptprogramm()
