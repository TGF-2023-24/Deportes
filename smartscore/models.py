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
    Pref_foot = models.CharField(max_length=50)
    Age = models.IntegerField()
    Height = models.IntegerField()	
    Weight = models.IntegerField()	
    Salary = models.IntegerField()	
    End_contract = models.DateField()
    CAbil = models.IntegerField()  #current ability
    Pot_abil = models.IntegerField()	 #potential ability
    Strater_match = models.IntegerField()
    Res_match = models.IntegerField()	
    Min = models.IntegerField()
    Goal = models.IntegerField()
    Asis = models.IntegerField()
    xG = models.FloatField() #expected goals
    Gol_90 = models.FloatField() #goals per 90 minutes
    Asis_90 = models.FloatField() #assists per 90 minutes
    Goal_allowed = models.IntegerField()	 #goals allowed
    Clean_sheet	= models.IntegerField() #clean sheets
    Sv_rat = models.IntegerField() #save rate over 100
    xSv_rat = models.IntegerField() #expected save rate over 100
    Pen_saved_rat	= models.IntegerField() #penalty saved rate over 100
    Faga = models.IntegerField() #fouls against
    Fcomm = models.IntegerField() #fouls made
    Yel = models.IntegerField() #yellow cards
    Red = models.IntegerField()     #red cards
    Dist_90	= models.FloatField() #distance covered per 90 minutes
    Key_tck_90 = models.FloatField() #key tackles per 90 minutes
    Key_hdr_90 = models.FloatField() #key headers per 90 minutes
    Blocks_90 = models.FloatField() #blocks per 90 minutes
    Clr_90 = models.FloatField() #clearances per 90 minutes
    Int_90 = models.FloatField() #interceptions per 90 minutes
    Hdr_rat = models.IntegerField() #headers won rate over 100
    Tackles_rat = models.IntegerField() #tackles won rate over 100
    Gl_mistake = models.IntegerField() #mistakes leading to goal
    Pass_rat = models.IntegerField() #pases completed rate over 100
    Pr_pass_90 = models.FloatField() #progressive passes rate over 100
    Key_pass_90 = models.FloatField() #key passes per 90 minutes
    Cr_c_90 = models.FloatField() #crosses created per 90 minutes
    Cr_c_acc = models.IntegerField() #crosses accuracy over 100
    Ch_c_90 = models.FloatField() #chances created per 90 minutes
    Drb_90 = models.FloatField() #dribbles per 90 minutes
    Poss_lost_90 = models.FloatField() #possession lost per 90 minutes
    Shot_rat = models.IntegerField() #shot rate over 100
    Conv_rat = models.IntegerField() #conversion rate over 100
    Dorsal = models.IntegerField() 
    Country_league = models.CharField(max_length=100) #country league


    def __str__(self):
        return self.Name
    
class Position(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name