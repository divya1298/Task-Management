from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Task, MonitoringLog

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'completed', 'user', 'assigned_to']

class MonitoringLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLog
        fields = ['task', 'checked_at', 'action_taken']

