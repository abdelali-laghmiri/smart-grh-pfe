from django.db import models
from django.utils import timezone
from users.models import UserProfile
from requests_engine.models import Request
# Create your models here.


# Notification model to store notifications for users
class Notification(models.Model):
    TYPE_CHOICES = [
        ('REQUEST', 'Request'),
        ('APPROVAL', 'Approval'),
        ('SYSTEM', 'System'),
    ]
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='info')
    related_request = models.ForeignKey(Request, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Notification for {self.user.username}: {self.type}'