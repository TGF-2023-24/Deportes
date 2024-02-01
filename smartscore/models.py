from django.db import models

# Create your models here.

class Player(models.Model):
    custom_id = models.IntegerField(primary_key=True)  # Define a custom primary key field
    Nombre = models.CharField(max_length=100)
    Nacionalidad = models.CharField(max_length=5)
    Internacionalidades = models.IntegerField()	
    Pos = models.CharField(max_length=50)
    Altura = models.IntegerField()	
    Peso = models.IntegerField()	
    Sueldo = models.IntegerField()	
    Final = models.DateField()	
    Part = models.IntegerField()	
    Enc = models.IntegerField()	
    Clean_sheet	= models.IntegerField()
    Pen_metidos_rat	= models.IntegerField()
    Dist_90	= models.IntegerField()
    Pep	= models.IntegerField()
    On_target_rat = models.IntegerField()

    def __str__(self):
        return self.Nombre