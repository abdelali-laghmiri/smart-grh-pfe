# apis for users app
from urllib import request
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Departement, JobPosition, Team, UserProfile
from .serializers import DepartmentSerializer, JobPositionSerializer, TeamSerializer, UserProfileSerializer, UserSerializer

# department API views
class DepartmentListCreateAPI(APIView):

    def get(self, request):
        departments = Departement.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# DepartmentDetailAPI for retrieving, updating, and deleting a specific department
class DepartmentDetailAPI(APIView):

    def get_object(self, pk):
        try:
            return Departement.objects.get(pk=pk)
        except Departement.DoesNotExist:
            return None

    def get(self, request, pk):
        department = self.get_object(pk)
        if not department:
            return Response({"error": "Not found"}, status=404)

        serializer = DepartmentSerializer(department)
        return Response(serializer.data)

    def put(self, request, pk):
        department = self.get_object(pk)
        if not department:
            return Response({"error": "Not found"}, status=404)

        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        department = self.get_object(pk)
        if not department:
            return Response({"error": "Not found"}, status=404)

        department.delete()
        return Response({"message": "Deleted successfully"}, status=204)
# JobPosition API views 
class JobPositionListCreateAPI(APIView):

    def get(self, request):
        positions = JobPosition.objects.all()
        serializer = JobPositionSerializer(positions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JobPositionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# JobPositionDetailAPI for retrieving, updating, and deleting a specific job position
class JobPositionDetailAPI(APIView):

    def get_object(self, pk):
        try:
            return JobPosition.objects.get(pk=pk)
        except JobPosition.DoesNotExist:
            return None

    def get(self, request, pk):
        position = self.get_object(pk)
        if not position:
            return Response({"error": "Not found"}, status=404)

        serializer = JobPositionSerializer(position)
        return Response(serializer.data)

    def put(self, request, pk):
        position = self.get_object(pk)
        if not position:
            return Response({"error": "Not found"}, status=404)

        serializer = JobPositionSerializer(position, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        position = self.get_object(pk)
        if not position:
            return Response({"error": "Not found"}, status=404)

        position.delete()
        return Response({"message": "Deleted"}, status=204)
    
# team api views 
class TeamListCreateAPI(APIView):

    def get(self, request):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
# TeamDetailAPI for retrieving, updating, and deleting a specific team
class TeamDetailAPI(APIView):

    def get_object(self, pk):
        try:
            return Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            return None

    def get(self, request, pk):
        team = self.get_object(pk)
        if not team:
            return Response({"error": "Not found"}, status=404)

        serializer = TeamSerializer(team)
        return Response(serializer.data)

    def put(self, request, pk):
        team = self.get_object(pk)
        if not team:
            return Response({"error": "Not found"}, status=404)

        serializer = TeamSerializer(team, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        team = self.get_object(pk)
        if not team:
            return Response({"error": "Not found"}, status=404)

        team.delete()
        return Response({"message": "Deleted"}, status=204)
## ------------USER AND USER PROPHILE SECTION -------------------


# user profile list and create API view

class UserProfileListCreateAPI(APIView):

    def get(self, request):
        Users =UserProfile.objects.all()
        serializer = UserProfileSerializer(Users, many=True)
        return Response(serializer.data)
    def post(self, request):
        usser_data = request.data.get('user')
        profile_data = request.data.copy()
        if not usser_data:
            return Response({"error": "User data is required"}, status=400)
        if User.objects.filter(username=usser_data.get('username')).exists():
            return Response(
                {"error": "Username already exists"},
                status=400
            )
        user = User.objects.create(
            username=usser_data.get('username'),
            email=usser_data.get('email'),
            
        )
        user.set_password("12345678")  # Set a default password (you should handle this properly in production)
        user.save()
        profile = UserProfile.objects.create(
            user=user,
            job_position_id=profile_data.get('job_position'),
            departement = get_object_or_404(
                                                Departement,
                                                id=profile_data.get('departement')
                                            ),
            team_id=profile_data.get('team'),
            manager_id=profile_data.get('manager'),
            leave_balance=profile_data.get('leave_balance', 0)
        )
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=201)

# user profile detail API view for retrieving, updating, and deleting a specific user profile
class UserProfileDetailAPI(APIView):
    def get_object(self, pk):
        try:
            return UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            return None
    def get(self, request, pk):
        profile = self.get_object(pk)
        if not profile:
            return Response({"error": "Not found"}, status=404)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
    def put(self, request, pk):
        profile = self.get_object(pk)
        if not profile:
            return Response({"error": "Not found"}, status=404)

        profile.job_position_id = request.data.get('job_position', profile.job_position_id)
        profile.departement_id = request.data.get('departement', profile.departement_id)
        profile.team_id = request.data.get('team', profile.team_id)
        profile.manager_id = request.data.get('manager', profile.manager_id)
        profile.leave_balance = request.data.get('leave_balance', profile.leave_balance)

        profile.save()

        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
    def delete(self, request, pk):
        profile = self.get_object(pk)
        if not profile:
            return Response({"error": "Not found"}, status=404)

        profile.delete()
        return Response({"message": "Deleted"}, status=204)
