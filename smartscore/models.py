from django.db import models

# Create your models here.

class Player(models.Model):
    custom_id = models.IntegerField(primary_key=True)  # Define a custom primary key field
    Name = models.CharField(max_length=100)
    Nacionality = models.CharField(max_length=5)
    International_match = models.IntegerField()
    Club = models.CharField(max_length=100)
    League = models.CharField(max_length=100)	
    Pos = models.ManyToManyField('Position')
    Leg = models.CharField(max_length=50)
    Age = models.IntegerField()
    Height = models.IntegerField()	
    Weight = models.IntegerField()	
    Salary = models.IntegerField()	
    End_contract = models.DateField()
    CAct = models.IntegerField() 
    CPot = models.IntegerField()	
    Strater_match = models.IntegerField()
    Res_match = models.IntegerField()	
    Min = models.IntegerField()
    Goal = models.IntegerField()
    Asis = models.IntegerField()
    xG = models.FloatField() #expected goals
    Gol_90 = models.FloatField() #goals per 90 minutes
    Asis_90 = models.FloatField() #assists per 90 minutes
    Enc = models.IntegerField()	 #
    Clean_sheet	= models.IntegerField() #clean sheets
    Pen_scored_rat	= models.IntegerField() #penalty scored rate over 100
    Fal_rec = models.IntegerField() #fouls received
    Fal_com = models.IntegerField() #fouls committed
    Ama = models.IntegerField() #yellow cards
    Roj = models.IntegerField()     #red cards
    Dist_90	= models.FloatField() #distance covered per 90 minutes
    Ent_clav = models.IntegerField() #entradas clave
    Err_clav = models.IntegerField() #errores claves
    Oc_C_90 = models.FloatField() #ocasiones creadas por 90 minutos
    Pas_Clv_90 = models.FloatField() #pases clave por 90 minutos
    Pep	= models.IntegerField() 
    On_target_rat = models.IntegerField() #on target rate over 100
    Tackles_won_rat = models.IntegerField() #tackles won rate over 100
    Reg_rat = models.IntegerField() #regate rate over 100
    Rp = models.IntegerField() 
    Pass_rat = models.IntegerField() #pases rate over 100
    Ent_rat = models.IntegerField() #entradas rate over 100
    Reg_90 = models.FloatField() #regates por 90 minutos
    Rob_90 = models.FloatField() #robos por 90 minutos


    def __str__(self):
        return self.Name
    
class Position(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name