from django.db import models
from users.models import UserProfile
# Create your models here.
# class Performance
class Performance(models.Model):
    employee = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='performances')
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    presence_rate = models.FloatField(default=0.0)
    dalay_rate = models.FloatField(default=0.0)
    aoutomatic_score = models.FloatField(default=0.0)
    evaluation_score = models.FloatField(null=True, blank=True)
    final_score = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('employee', 'month', 'year')
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.employee.user.username} - {self.month}/{self.year}"