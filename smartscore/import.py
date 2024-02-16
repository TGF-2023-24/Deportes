import csv
from smartscore.models import Player, Position
from datetime import datetime
from .utils import get_player_positions # Import the function from utils.py

with open('new_short_dataset.csv',  encoding='utf-8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV)  
    for row in readCSV:
        player = Player()
        player.custom_id = int(row[0])
        player.Name = row[2]
        player.Nationality = row[3]
        player.International_match = int(row[4].replace(',', ''))  # Eliminar comas en números
        player.Club = row[6]
        player.League = row[7]
        player.Pref_foot = row[9]
        player.Age = int(row[10])
        player.Height = int(row[11].split()[0].replace(',', ''))  # Extraer solo el número de la altura
        player.Weight = int(row[12].split()[0])  # Extraer solo el número del peso
        player.Salary = int(row[13].split()[0].replace('.', '').replace('€', ''))  # Eliminar puntos y extraer solo el número
        player.End_contract = datetime.strptime(row[14], '%d/%m/%Y').date()  # Convertir fecha al formato correcto
        player.CAbil = int(row[15])
        player.Pot_abil = int(row[16])
        player.Strater_match = 0 if row[17] == '-' else int(row[17].split()[0])  # Extraer solo el número de partidos
        player.Res_match = int(row[18])
        player.Min = 0 if row[17] == '-' else int(row[19].replace('.', ''))  # Eliminar comas en números
        player.Goal = 0 if row[17] == '-' else int(row[20])
        player.Asis = 0 if row[17] == '-' else int(row[21])
        player.xG = 0 if row[17] == '-' else float(row[22].replace(',', '.'))
        player.Gol_90 = 0 if row[23] == '-' else float(row[23].replace(',', '.'))
        player.Asis_90 = 0 if row[24] == '-' else float(row[24].replace(',', '.'))
        player.Goal_allowed = 0 if row[25] == '-' else int(row[25])  # Convertir '-' a 0
        player.Clean_sheet = 0 if row[26] == '-' else int(row[26])  # Convertir '-' a 0
        player.Sv_rat = 0 if row[27] == '-' else int(row[27].replace('%', ''))
        player.xSv_rat = 0 if row[28] == '-' else int(row[28].replace('%', ''))
        player.Pen_saved_rat = 0 if row[29] == '-' else int(row[29].replace('%', ''))
        player.Faga = 0 if row[17] == '-' else int(row[30])
        player.Fcomm = 0 if row[17] == '-' else int(row[31])
        player.Yel = 0 if row[17] == '-' else int(row[32])
        player.Red  = 0 if row[17] == '-' else int(row[33])
        player.Dist_90 = 0 if row[17] == '-' else float(row[34].split()[0].replace(',', '.').replace('km', ''))
        player.Key_tck_90 = 0 if row[35] == '-' else float(row[35].replace(',', '.').split()[0])
        player.Key_hdr_90 = 0 if row[36] == '-' else float(row[36].replace(',', '.').split()[0])
        player.Blocks_90 = 0 if row[37] == '-' else float(row[37].replace(',', '.').split()[0])
        player.Clr_90 = 0 if row[38] == '-' else float(row[38].replace(',', '.').split()[0])
        player.Int_90 = 0 if row[39] == '-' else float(row[39].replace(',', '.').split()[0])
        player.Hdr_rat = 0 if row[40] == '-' else int(row[40].replace('%', ''))
        player.Tackles_rat = 0 if row[41] == '-' else int(row[41].replace('%', ''))
        player.Gl_mistake = 0 if row[17] == '-' else int(row[42])
        player.Pass_rat = 0 if row[43] == '-' else int(row[43].replace('%', ''))
        player.Pr_pass_90 = 0 if row[44] == '-' else float(row[44].replace(',', '.'))
        player.Key_pass_90 = 0 if row[45] == '-' else float(row[45].replace(',', '.'))
        player.Cr_c_90 = 0 if row[46] == '-' else float(row[46].replace(',', '.').split()[0])
        player.Cr_c_acc = 0 if row[47] == '-' else int(row[47].replace('%', ''))
        player.Ch_c_90 = 0 if row[48] == '-' else float(row[48].replace(',', '.').split()[0])
        player.Drb_90 = 0 if row[49] == '-' else float(row[49].replace(',', '.').split()[0])
        player.Poss_lost_90 = 0 if row[50] == '-' else float(row[50].replace(',', '.').split()[0])
        player.Shot_rat = 0 if row[51] == '-' else int(row[51].replace('%', ''))
        player.Conv_rat = 0 if row[52] == '-' else int(row[52].replace('%', ''))
        player.Dorsal = 0 if row[53] == '-' else int(row[53])
        
        
        player.Country_league = row[54].split()[0]  # Extraer solo el nombre del país

        player.save()

        # Obtener las posiciones del jugador
        positions = get_player_positions(row[8])

        # Crear instancias de las posiciones y agregarlas al jugador
        for position_name in positions:
            position, created = Position.objects.get_or_create(name=position_name)
            player.Pos.add(position)

        player.save()