from django.db import models
from django.contrib.auth.models import User

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

# class Team 
class Team(models.Model):
    name = models.CharField(max_length=255)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, related_name='teams')

    def __str__(self):
        return f"{self.name} ({self.departement})"
    

# class UserProfile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    job_position = models.ForeignKey(JobPosition, on_delete=models.SET_NULL, null=True, related_name='users')
    departement = models.ForeignKey(Departement, on_delete=models.SET_NULL, null=True, related_name='users')
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')
    leave_balance = models.FloatField(default=0.0)
    def __str__(self):
        return self.user.username

# class Leave Adjustment
class LeaveAdjustment(models.Model):
    employee = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='leave_adjustments')
    ajusted_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name='adjustments_made')
    amount = models.FloatField()
    reason = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.user.username} | {self.amount}"
    

    