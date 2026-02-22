from rest_framework import serializers
from .models import (
    Departement,
    JobPosition,
    Team,
    LeaveAdjustment,
    UserProfile)

# serializer for department 
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departement
        fields = '__all__'



# serializer for job position
class JobPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosition
        fields = '__all__'

# serializer for team
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'