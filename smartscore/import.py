import csv
from smartscore.models import Player
from datetime import datetime

with open('Dataset_comp_acortado.csv',  encoding='utf-8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV)  # Saltar la primera fila que contiene los encabezados
    #ID,nada,Nombre,Nac,Internacionalidades,nada2,Club,Liga,Pos,row 0-8
    #Pierna_buena,Edad,Altura,Peso,Sueldo,Final, 9-14
    #CAct,CPot,Strater_game,Res_game,Min,Gol,Asis, 15-21
    #xG,Gol_90,Asis_90,Enc,Clean_sheet,Pen_metidos_rat,Fal_rev,Fal_com,Ama,Roj,Dist_90, 22-32
    #Ent_clav,Err_clav,Oc_C_90,Pas_Clv_90,Pep,On_target_rat,Tackles_won_rat,Reg_rat,Rp,Pass_rat,Ent_rat,Reg_90,Rob_90
    for row in readCSV:
        player = Player()
        player.custom_id = int(row[0])
        player.Name = row[2]
        player.Nacionality = row[3]
        player.International_match = int(row[4].replace(',', ''))  # Eliminar comas en números
        player.Club = row[6]
        player.League = row[7]
        player.Pos = row[8]
        player.Leg = row[9]
        player.Age = int(row[10])
        player.Height = int(row[11].split()[0])  # Extraer solo el número de la altura
        player.Weight = int(row[12].split()[0])  # Extraer solo el número del peso
        player.Salary = int(row[13].split()[0].replace('.', ''))  # Eliminar puntos y extraer solo el número
        player.End_contract = datetime.strptime(row[14], '%d/%m/%Y').date()  # Convertir fecha al formato correcto
        player.CAct = int(row[15])
        player.CPot = int(row[16])
        player.Strater_match = int(row[17].split()[0])  # Extraer solo el número de partidos
        player.Res_match = int(row[18])
        player.Min = int(row[19].replace('.', ''))  # Eliminar comas en números
        player.Goal = int(row[20])
        player.Asis = int(row[21])
        player.xG = float(row[22].replace(',', '.'))
        player.Gol_90 = 0 if row[23] == '-' else float(row[23].replace(',', '.'))
        player.Asis_90 = 0 if row[24] == '-' else float(row[24].replace(',', '.'))
        player.Enc = 0 if row[25] == '-' else int(row[25])  # Convertir '-' a 0
        player.Clean_sheet = 0 if row[26] == '-' else int(row[26])  # Convertir '-' a 0
        player.Pen_scored_rat = 0 if row[27] == '-' else int(row[27].replace('%', ''))
        player.Fal_rec = int(row[28])
        player.Fal_com = int(row[29])
        player.Ama = int(row[30])
        player.Roj = int(row[31])
        player.Dist_90 = float(row[32].replace(',', '.').split()[0])
        player.Ent_clav = int(row[33])
        player.Err_clav = int(row[34])
        player.Oc_C_90 = 0 if row[35] == '-' else float(row[35].replace(',', '.').split()[0])
        player.Pas_Clv_90 = 0 if row[36] == '-' else float(row[36].replace(',', '.').split()[0])
        player.Pep = 0 if row[37] == '-' else int(row[37].replace('%', ''))  # Convertir '-' a 0
        player.On_target_rat = 0 if row[38] == '-' else int(row[38].replace('%', ''))  # Eliminar '%' en la tasa de acierto
        player.Tackles_won_rat = 0 if row[39] == '-' else int(row[39].replace('%', ''))  # Eliminar '%' en la tasa de acierto
        player.Reg_rat = 0 if row[40] == '-' else int(row[40].replace('%', ''))
        player.Rp = 0 if row[41] == '-' else int(row[41].replace('%', ''))
        player.Pass_rat = 0 if row[42] == '-' else int(row[42].replace('%', ''))
        player.Ent_rat = 0 if row[43] == '-' else int(row[43].replace('%', ''))
        player.Reg_90 = 0 if row[44] == '-' else float(row[44].replace(',', '.'))
        player.Rob_90 = 0 if row[45] == '-' else float(row[45].replace(',', '.'))
        player.save() 
