import csv
from smartscore.models import Player
from datetime import datetime

with open('dataset.csv',  encoding='utf-8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV)  # Saltar la primera fila que contiene los encabezados
    for row in readCSV:
        player = Player()
        player.custom_id = int(row[0])
        player.Nombre = row[2]
        player.Nacionalidad = row[3]
        player.Internacionalidades = int(row[4].replace(',', ''))  # Eliminar comas en números
        player.Pos = row[5]
        player.Altura = int(row[6].split()[0])  # Extraer solo el número de la altura
        player.Peso = int(row[7].split()[0])  # Extraer solo el número del peso
        player.Sueldo = int(row[8].split()[0].replace('.', ''))  # Eliminar puntos y extraer solo el número
        player.Final = datetime.strptime(row[9], '%d/%m/%Y').date()  # Convertir fecha al formato correcto
        player.Part = int(row[10].split()[0])  # Extraer solo el número de partidos
        player.Enc = 0 if row[11] == '-' else int(row[11])  # Convertir '-' a 0
        player.Clean_sheet = 0 if row[12] == '-' else int(row[12])  # Convertir '-' a 0
        player.Pen_metidos_rat = 0 if row[13] == '-' else int(row[13].replace('%', ''))
        player.Dist_90 = int(row[14].split()[0].replace(',', ''))  # Eliminar comas y extraer solo el número
        player.Pep = 0 if row[15] == '-' else int(row[15].replace('%', ''))  # Convertir '-' a 0
        player.On_target_rat = 0 if row[16] == '-' else int(row[16].replace('%', ''))  # Eliminar '%' en la tasa de acierto
        player.save() 
