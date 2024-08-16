from rest_framework import serializers
from .models import TeacherDetails
from django.contrib.auth import get_user_model

User = get_user_model()

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherDetails
        fields = '__all__'
        read_only_fields = ['teacher_id']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','password','company','terms_and_condition','role','is_active')
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            company=validated_data['company'],
            terms_and_condition=validated_data['terms_and_condition'],
            role=validated_data.get('role',[]),
            is_active=validated_data.get('is_active',True)
        )

        return user