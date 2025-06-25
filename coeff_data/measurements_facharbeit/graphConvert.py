from math import sin

offset = 5

readFile = input("Dateiname: ")
seperator = input("Seperator für Kommazahlen (Standart: ,): ")
if seperator == "":
    seperator = ","
valuesTogether = int(input("Werte zusammenfassen: "))
writeFile = input("Dateiname für Export: ")


# Processing
print("Datei öffnen")
file = open(readFile,"r")
print("Inhalt lesen")
lines = file.readlines()
file.close()
print("Inhalt vorverarbeiten")
head = lines[:offset]
lines = lines[offset:]

values = []

print("Inhalt einlesen")
for line in lines:
    value = float(line[line.index("\t") + 1:-1].replace(",","."))
    values.append(value)

newValues = []


print("Text für neue Datei generieren")
while len(values) > 0:
    if len(values) >= valuesTogether:
        newValue = sum(values[:valuesTogether]) / valuesTogether
        newValues.append(str(round(newValue,3)).replace(".",seperator))
        values = values[valuesTogether:]
    else:
        newValue = sum(values) / len(values)
        newValues.append(str(round(newValue,3)).replace(".",seperator))
        break

for i in range(0,len(values),100):
    #newValues.append(str(values[i]))
    newValues.append(str(i*90/36000) + "\t" + str(values[i]) + "\t" + str(values[i]*15.701/(sin(i*90/36000*2*3.1415926/360)+0.000000001)))


print("Neue Datei öffnen oder erstellen")
exportFile = open(writeFile,"w")
print("Daten für Datei zusammenfügen")
#exportFile.write(readFile + ": Vereinte Werte: " + str(valuesTogether) + "\n")
#exportFile.writelines(head)
exportFile.write("\n".join(newValues))
print("Daten in die Datei schreiben")
exportFile.truncate()
exportFile.close()
input("Datei konvertiert!\nZum Verlassen ENTER drücken")
