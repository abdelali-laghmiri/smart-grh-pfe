from django.db import models

# Create your models here.


# class Departement 
class Departement(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# class Job Position
class JobPosition(models.Model):
    titre = models.CharField(max_length=100 , unique=True)
    level = models.IntegerField()
    montlhy_leave_accrual = models.FloatField(default=1.5)
    def __str__(self):
        return f"{self.titre} (Level {self.level})"

# 

    