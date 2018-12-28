from Kamerasteuerung import schiesseFoto, blinken   # Hier werden einzelne Module importiert,
from tkinter import *                               # sie werden für das Programm später benötigt.
from time import *
import _thread
import os, pickle
import matplotlib.pyplot as plt

einheiten = ["s","min","h","d"]                     # Dort werden globale Variablen deklariert. 
faktoren = [1,60,3600,86400]                        # Global heißt, dass alle Funktionen
start = False                                       # und ähnliches hier zugreifen können.
startZeit = 0
zeit = 0

def Verzeichniswaehlen():                           # Das ist die Funktion, wo das Verzeichnis
    v = filedialog.askdirectory()                   # des Projektes gewählt wird.
    textVerzeichnis.delete(1.0,END)
    textVerzeichnis.insert(1.0,v+"/")

def check():                                                        # Die Funktion „check“ dient zur Kontrolle,
    v = textVerzeichnis.get(1.0,END)[:-1]                           # ob das gewählte Verzeichnis überhaupt existiert.
    if os.path.isdir(v):                                            # Falls dieses nämlich nicht existieren,
        messagebox.showinfo(message="Dieses Verzeichnis existiert") # besteht die Möglichkeit dieses direkt zu erzeugen.
    else:
        if messagebox.askyesno(message="Dieses Verzeichnis existiert nicht. Wollen sie dieses Verzeichnis erzeugen?"):
            os.makedirs(v)
        else:
            messagebox.showinfo(message="Bitte ändern sie das Verzeichnis")
        
    

def Start():                    # Mit dieser Funktion wird
    global start, startZeit     #e in Projekt gestartet oder gestoppt.
    if start == False:
        startZeit = time()
        start = True
    else:
        start = False

def Interval():                         # Hier wird mithilfe der Funktion
    global einheiten,faktoren           # die Einstellung des Intervalls unternommen.
    ersteEinheit = einheiten.pop(0)
    ersterFaktor = faktoren.pop(0)
    einheiten.append(ersteEinheit)
    faktoren.append(ersterFaktor)
    buttonInterval.config(text=einheiten[0])

def Bilder():                           # In der Funktion „Bilder“ wird
    global zeit                         # die Bilderstellung nach Intervall gesteuert,
    letzteZeit = 0                      # die Bilder werden nach Zeitpunkt abgespeichert,
    bildAnzahl = 0                      # auf der Benutzeroberfläche angezeigt und
    while True:                         # die Anzahl der Bilder wird erhöht.
        zeitInt = int(zeit)             # Diese Funktion läuft über einen Thread,
        if start:                       # das bedeutet, dass die Funktion neben
            faktor = faktoren[0]        # dem eigentlichen Programm laufen kann.
            interval = textInterval.get(1.0,END)[:-1]
            interval = float(interval) * faktor
            verzeichnis = textVerzeichnis.get(1.0,END)[:-1]
            if os.path.isdir(verzeichnis):
                if zeitInt - (letzteZeit) + int(interval/10) >= interval:)
                    blinken(int(interval/10))
                    timedata = [str(localtime().tm_mday),str(localtime().tm_mon),str(localtime().tm_year),str(localtime().tm_hour),str(localtime().tm_min),str(localtime().tm_sec)]
                    for c in range(len(timedata)):
                        if len(timedata[0]) < 2:
                            g = "0"+timedata[0]
                            del timedata[0]
                            timedata.append(g)
                        else:
                            g = timedata[0]
                            del timedata[0]
                            timedata.append(g)
                    BildZeit = "".join(timedata)
                    schiesseFoto(400,300,verzeichnis+"img_"+BildZeit+".png",verzeichnis)
                    letzteZeit = zeitInt + int(interval/10)
                    labelDatum.config(text=asctime())
                    letztesBild = PhotoImage(master=window,file=verzeichnis+"img_"+BildZeit+".png")
                    letztesBild = letztesBild.subsample(2)
                    labelLetztesBild.config(image=letztesBild)
                    bildAnzahl += 1
                    labelAnzahlBilder.config(text="Anzahl der Bilder: "+str(bildAnzahl))
            else:
                messagebox.showerror(message="Das Verzeichnis existiert nicht!")
        else:
            bildAnzahl = 0
            letzteZeit = 0
            labelAnzahlBilder.config(text="Anzahl der Bilder: "+str(bildAnzahl))    
        sleep(0.01)

def Zeitanpassung():                    # Auch diese Funktion wird über einen Thread angesteuert. 
    global zeit                         # Sie bewirkt, dass die vergangene Zeit des Timers richtig
    while True:                         # auf den dafür konzipierten Bereich angezeigt wird und
        if start:                       # dass die Zeit vor allem für die Funktion „Bilder“,
            zeit = time() - startZeit   # die die vergangene Zeit zur Berechnung, wann ein Bild
            zeit = round(zeit,4)        # gemacht werden soll, benötigt, zur Verfügung steht.
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

def Video():                                        # Die Funktion „Video“ erstellt eine Animation    
    fps = 100.0                                     # des Pflanzenwachstums durch die Bilder.
    verzeichnis = None                              # Hier wird das Programm „feh“ verwendetet.
    fps = float(textFps.get(1.0,END)[:-1])          # Außerdem muss hier eine Anzahl von FPS (frames per second)
    verzeichnis = textVerzeichnis.get(1.0,END)[:-1] # und das Verzeichnis angegeben werden.
    if os.path.isdir(verzeichnis):
        command = "feh -Y -x -q -D "+str(1/fps)+" -B black -F -Z -d "+verzeichnis+"*"
        os.system(command)
    else:
        messagebox.showerror(message="Das Verzeichnis existiert nicht!")

def Messwerte():                                        # Mithilfe von dieser Funktion „Messwerte“
    einheit = einheiten[0]                              # können die Messdaten des Sensor-Moduls,
    interval = int(textInterval.get(1.0,END)[:-1])      # welche in einer Datei abgespeichert sind,
    verzeichnis = None                                  # gelesen werden. Diese werden dann so geordnet,
    verzeichnis = textVerzeichnis.get(1.0,END)[:-1]     # dass mit dem Programm „Pyplot“ Graphen
    if os.path.exists(verzeichnis+"Messwerte.dat"):     # aus den Messwerten erstellt werden können.
        h = open(verzeichnis+"Messwerte.dat","rb")      # Hierzu ist auch das Intervall wichtig,
        messwerte = pickle.load(h)                      # um die richtigen Zeitabstände in den Graphen
        h.close()                                       # wiederzugeben. Auch ein Durchschnittsmesswert
        x = []                                          # wird für die jeweilige Kategorie mitgegeben.
        for i in range(1,len(messwerte)+1):
            x.append(i*interval)
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
        yT = []
        yLf = []
        yLd = []
        w = 3
        for i in messwerteneu:
            if w % 3 == 0:
                yT.append(i)
            elif w % 3 == 1:
                yLf.append(i)
            elif w % 3 == 2:
                yLd.append(i)
            w += 1
        fig,p = plt.subplots(3, 1,num='JuFo')
        p[0].plot(x,yT,'ro-')
        p[0].set_title('Temperatur')
        p[0].set_ylabel('°C')
        
        p[1].plot(x,yLf,'go-')
        p[1].set_title('Luftdruck')
        p[1].set_ylabel('hPa')
        
        p[2].plot(x,yLd,'bo-')
        p[2].set_title('Luftfeuchtigkeit')
        p[2].set_ylabel('%')
        p[2].set_xlabel('Zeit ('+einheit+')')

        plt.tight_layout(pad=0.4,w_pad=0.5,h_pad=1.0)
        plt.show()
    else:
        messagebox.showerror(message="Die Messwerte.dat-Datei existiert nicht!")

def Hauptprogramm():
    global window,labelAnzahlBilder,buttonInterval,labelZeit,letztesBild,labelLetztesBild,labelDatum,textInterval,textVerzeichnis,textFps
    window = Tk()
    window.title("Das Geheimnis des Wachstums")                     # Diese letzte Funktion ist die Hauptfunktion,
    letztesBild = None                                              # hier werden alle anderen Funktionen in einer
    labelLetztesBild = Label(master=window,font=("Arial",14),       # graphischen Benutzeroberfläche mithilfe von dem 
                             text="Keine Bilder")                   # Python-Modul „tkinter“ zusammengenommen.
    labelLetztesBild.grid(column=2,row=0,columnspan=10,rowspan=11)  # Einzelne Buttons, Labels und Textfelder
    labelDatum = Label(master=window,font=("Arial",14))             # werden hier erstellt und den Funktionen
    labelDatum.grid(column=2,row=11,columnspan=10)                  # zugewiesen, welche dann Interaktionen
    labelVerzeichnis = Label(master=window,font=("Arial",14),       # hervorrufen. Diese Elemente werden dann
                             text="Verzeichnis")                    # in einem Gitter angeordnet,
    labelVerzeichnis.grid(column=0,row=1,sticky=W)                  # das macht das Layout aus.
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
                               width=22,font=("arial",14),command=Messwerte)
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
    _thread.start_new_thread(Zeitanpassung,())
    _thread.start_new_thread(Bilder,())
    window.mainloop()
    
Hauptprogramm()
