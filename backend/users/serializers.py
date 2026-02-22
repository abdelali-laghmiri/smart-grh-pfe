from rest_framework import serializers
from django.contrib.auth.models import User
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

## ------------USER AND USER PROPHILE SECTION -------------------
# serializer for user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
# serializer for user profile

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = '__all__'

    def validate(self, data):
        user_data = data.get('user')

        if User.objects.filter(username=user_data.get('username')).exists():
            raise serializers.ValidationError(
                {"username": "This username already exists."}
            )

        return data


