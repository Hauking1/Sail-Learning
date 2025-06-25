from math import sin, radians

offset = 5 #Startzeile der Daten
readFile = "F_W; alpha laufend 0-360°; Profil1.txt" #Eingabedatei
seperator = "." #Fließkommaseperator
valuesTogether = 800 #Anzahl der Kombinierten Werte
maxX = 360 #maximaler X-Wert
writeFile = "out.txt" #Ausgabedatei

def kraftToCw (xWert, yWert):
    if xWert == 0:
        winkelDingens = 0.00001
    else:
        winkelDingens = sin(radians(xWert))
    return yWert * 15.701 / winkelDingens


# Processing
print("Datei öffnen")
file = open(readFile,"r")
print("Inhalt lesen")
lines = file.readlines()
file.close()
print("Inhalt vorverarbeiten")
head = lines[:offset]
lines = lines[offset:]
indexToX = maxX / len(lines)

values = []

print("Inhalt einlesen")
for line in lines:
    value = float(line[line.index("\t") + 1:-1].replace(",","."))
    values.append(value)

dataMatrix = []


print("Text für neue Datei generieren")
i = 0
while i + valuesTogether <= len(values):
    xWert = (i + valuesTogether / 2) * indexToX
    yWert = sum(values[i:i + valuesTogether]) / valuesTogether
    line = []
    line.append(xWert)
    line.append(yWert)
    line.append(kraftToCw(xWert, yWert))
    
    dataMatrix.append(line)
    i = i + valuesTogether

out = ""

for dataLine in dataMatrix:
    line = ""
    for data in dataLine:
        line += str(data) + "\t"
    line = line[:-1]
    out += line + "\n"

print("Neue Datei öffnen oder erstellen")
exportFile = open(writeFile,"w")
print("Daten für Datei zusammenfügen")
#exportFile.write(readFile + ": Vereinte Werte: " + str(valuesTogether) + "\n")
#exportFile.writelines(head)
exportFile.write(out)
print("Daten in die Datei schreiben")
exportFile.truncate()
exportFile.close()
input("Datei konvertiert!\nZum Verlassen ENTER drücken")
