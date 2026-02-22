from django.db import models
from django.utils import timezone
from users.models import JobPosition ,Departement,UserProfile
# Create your models here.

# class Request Type
class RequestType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

# class Approval Workflow
class ApprovalWorkflow(models.Model):
    request_type = models.OneToOneField(RequestType, on_delete=models.CASCADE, related_name='approval_workflow')

    def __str__(self):
        return f"Workflow for {self.request_type.name}"
    

# Approval Step
class ApprovalStep(models.Model):
    workflow = models.ForeignKey(ApprovalWorkflow, on_delete=models.CASCADE, related_name='steps')
    step_order = models.PositiveIntegerField()
    required_position = models.ForeignKey(JobPosition, on_delete=models.CASCADE, related_name='approval_steps')
    use_hierarchy = models.BooleanField(default=False)
    restricted_departement = models.ForeignKey(Departement, on_delete=models.CASCADE, related_name='approval_steps', null=True, blank=True)
    # using class meta to order the steps by step_order and to ensure that each step order is unique within a workflow
    class Meta:
        ordering = ['step_order']
        unique_together = ('workflow', 'step_order')
    
    def __str__(self):
        return f"Step {self.step_order} for {self.workflow.request_type.name}"
    

# class Request
class Request(models.Model):
    STATUS_CHOICES = [
            ('PENDING', 'Pending'),
            ('APPROVED', 'Approved'),
            ('REJECTED', 'Rejected'),
            ('CANCELLED', 'Cancelled'),
         ]
    submetted_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='requests')
    request_type = models.ForeignKey(RequestType, on_delete=models.CASCADE, related_name='requests')
    submission_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    cuurent_step = models.PositiveIntegerField(default=1)
    cancellation_reason = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.request_type.name} - {self.submetted_by.user.username}"

# class Approval History
class ApprovalHistory(models.Model):
    DSISION_CHOICES = [
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='history')
    approved_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name='approvals')
    decision = models.CharField(max_length=20, choices=DSISION_CHOICES)
    comment = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.request} - {self.decision} by {self.approved_by.user.username if self.approved_by else 'Unknown'}"
