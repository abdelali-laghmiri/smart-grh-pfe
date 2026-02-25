# API views for the requests engine
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import RequestType, ApprovalWorkflow,ApprovalStep,Request, ApprovalHistory
from .serializers import RequestTypeSerializer, ApprovalWorkflowSerializer,ApprovalStepSerializer,RequestSerializer, ApprovalHistorySerializer
from django.shortcuts import get_object_or_404
from .services import find_hierarchical_approver
from users.models import UserProfile
#------- request types API views -------
# API views for RequestType
class RequestTypeListCreateAPI(APIView):

    def get(self, request):
        types = RequestType.objects.all()
        serializer = RequestTypeSerializer(types, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RequestTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# API view for retrieving, updating, and deleting a specific RequestType
class RequestTypeDetailAPI(APIView):

    def get_object(self, pk):
        try:
            return RequestType.objects.get(pk=pk)
        except RequestType.DoesNotExist:
            return None

    def get(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not found"}, status=404)

        serializer = RequestTypeSerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not found"}, status=404)

        serializer = RequestTypeSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not found"}, status=404)

        obj.delete()
        return Response({"message": "Deleted"}, status=204)
    
# ------- end of request types API views -------

#------- approval workflows API views -------
# API views for ApprovalWorkflow
class ApprovalWorkflowListCreateAPI(APIView):

    def get(self, request):
        workflows = ApprovalWorkflow.objects.all()
        serializer = ApprovalWorkflowSerializer(workflows, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ApprovalWorkflowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
# API view for retrieving, updating, and deleting a specific ApprovalWorkflow
class ApprovalWorkflowDetailAPI(APIView):
    def get_object(self, pk):
        try:
            return ApprovalWorkflow.objects.get(pk=pk)
        except ApprovalWorkflow.DoesNotExist:
            return None

    def get(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not found"}, status=404)

        serializer = ApprovalWorkflowSerializer(obj)
        return Response(serializer.data)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not found"}, status=404)

        obj.delete()
        return Response({"message": "Deleted"}, status=204)
# ------- end of approval workflows API views -------


# ------- approval steps API views -------
# API views for ApprovalStep
class ApprovalStepListCreateAPI(APIView):
    def get(self, request):
        steps = ApprovalStep.objects.all()
        serializer = ApprovalStepSerializer(steps, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ApprovalStepSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
# API view for retrieving, updating, and deleting a specific ApprovalStep
class ApprovalStepDetailAPI(APIView):
    def get_object(self, pk):
        try:
            return ApprovalStep.objects.get(pk=pk)
        except ApprovalStep.DoesNotExist:
            return None
    def get(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not found"}, status=404)

        serializer = ApprovalStepSerializer(obj)
        return Response(serializer.data)
    def put(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not found"}, status=404)

        serializer = ApprovalStepSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)
    def delete(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not found"}, status=404)

        obj.delete()
        return Response({"message": "Deleted"}, status=204)
# ------- end of approval steps API views -------
# ------- requests API views -------
# API views for Request
class RequestListCreateAPI(APIView):
    def get(self, request):
        requests = Request.objects.all()
        serializer = RequestSerializer(requests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
# API view for retrieving, updating, and deleting a specific Request
class RequestDetailAPI(APIView):
    def get_object(self, pk):
        try : 
            return Request.objects.get(pk=pk)
        except Request.DoesNotExist:
            return None
    def get(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not found"}, status=404)

        serializer = RequestSerializer(obj)
        return Response(serializer.data)
    def put(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not found"}, status=404)

        serializer = RequestSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)
    
# ------- end of requests API views -------
# ------- Approve Request API views -------

class ApproveRequestAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        req = get_object_or_404(Request, pk=pk)

        #  current step
        step = ApprovalStep.objects.get(
            workflow=req.request_type.workflow,
            step_order=req.current_step
        )

        employee = req.submitted_by
        required_position = step.required_position

        #  apply_hierarchy
        if step.apply_hierarchy:
            approver = find_hierarchical_approver(
                employee,
                required_position
            )
        else:
            approver = UserProfile.objects.filter(
                job_position=required_position
            ).first()

        if not approver:
            return Response(
                {"error": "No valid approver found"},
                status=400
            )
        print("Approver found:", approver.user.username)
        # approver
        if request.user != approver.user:
            return Response(
                {"error": "You are not authorized to approve this request"},
                status=403
            )
        
        # Move to next step
        next_step = ApprovalStep.objects.filter(
            workflow=req.request_type.workflow,
            step_order=req.current_step + 1
        ).first()

        if next_step:
            req.current_step += 1
            req.save()
            return Response({"message": "Moved to next step"})
        else:
            req.status = "APPROVED"
            req.save()
            return Response({"message": "Request fully approved"})