from rest_framework import serializers
from .models import Departement,JobPosition


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departement
        fields = '__all__'




class JobPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosition
        fields = '__all__'