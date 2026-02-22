from django.db import models
from django.utils import timezone
from users.models import  UserProfile
# Create your models here.

# class Attendance
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('PRESENT', 'Present'),
        ('LATE', 'Late'),
        ('ABSENT', 'Absent'),
    ]
    employee = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=timezone.now)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PRESENT')
    class Meta:
        unique_together = ('employee', 'date')
        ordering = ['-date']
    def __str__(self):
        return f"{self.employee.user.username} - {self.date} - {self.status}"