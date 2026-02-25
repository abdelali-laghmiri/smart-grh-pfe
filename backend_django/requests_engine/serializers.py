from rest_framework import serializers
from .models import RequestType, ApprovalWorkflow, Request, ApprovalHistory,ApprovalStep

# Serializer for the RequestType model
class RequestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestType
        fields = '__all__'
# Serializer for the ApprovalWorkflow model
class ApprovalWorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalWorkflow
        fields = '__all__'
# Serializer for the Request model
class RequestSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Request
        fields = '__all__'
# Serializer for the ApprovalHistory model
class ApprovalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalHistory
        fields = '__all__'
# Serializer for the ApprovalStep model
class ApprovalStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalStep
        fields = '__all__'
