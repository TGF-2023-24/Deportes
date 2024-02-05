from django.db import models

# Create your models here.

class Player(models.Model):
    custom_id = models.IntegerField(primary_key=True)  # Define a custom primary key field
    Name = models.CharField(max_length=100)
    Nacionality = models.CharField(max_length=5)
    International_match = models.IntegerField()
    Club = models.CharField(max_length=100)
    League = models.CharField(max_length=100)	
    Pos = models.CharField(max_length=50)
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
    xG = models.FloatField()
    Gol_90 = models.FloatField()
    Asis_90 = models.FloatField()
    Enc = models.IntegerField()	
    Clean_sheet	= models.IntegerField()
    Pen_scored_rat	= models.IntegerField()
    Fal_rec = models.IntegerField()
    Fal_com = models.IntegerField()
    Ama = models.IntegerField()
    Roj = models.IntegerField()
    Dist_90	= models.FloatField()
    Ent_clav = models.IntegerField()
    Err_clav = models.IntegerField()
    Oc_C_90 = models.FloatField()
    Pas_Clv_90 = models.FloatField()
    Pep	= models.IntegerField()
    On_target_rat = models.IntegerField()
    Tackles_won_rat = models.IntegerField()
    Reg_rat = models.IntegerField()
    Rp = models.IntegerField()
    Pass_rat = models.IntegerField()
    Ent_rat = models.IntegerField()
    Reg_90 = models.FloatField()
    Rob_90 = models.FloatField()


    def __str__(self):
        return self.Name