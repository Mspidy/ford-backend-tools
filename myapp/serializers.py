from rest_framework import serializers
from .models import TeacherDetails

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherDetails
        fields = '__all__'
        read_only_fields = ['teacher_id']