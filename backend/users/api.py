# apis for users app
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Departement, JobPosition, Team
from .serializers import DepartmentSerializer, JobPositionSerializer, TeamSerializer

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