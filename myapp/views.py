from django.shortcuts import render
from .models import TeacherDetails
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TeacherDetails
from django.http import FileResponse
import pandas as pd
import os
from django.conf import settings
from datetime import datetime
from django.contrib.auth import get_user_model, authenticate
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
User = get_user_model()

def google_login(request):
    return redirect('/auth/login/google-oauth2/')

class UserRegisteration(APIView):
    def post(self,request):
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            return Response({'error':'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response({'token': token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            # Serialize user data
            user_serializer = UserSerializer(user)
            return Response({'token':token, 'user': user_serializer.data,'message':'Login Successfully.'})
        else:
            return Response({'error':'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Create your views here.
class TeacherDetailsListCreateAPIView(APIView):
    def get(self, request, format=None):
        teachers = TeacherDetails.objects.all().order_by('id')
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BulkTeacherUploadView(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        try:
            data = pd.read_excel(file)
            for _, row in data.iterrows():
                dob_str = row['date_of_birth'].strftime('%d-%m-%Y') if isinstance(row['date_of_birth'], pd.Timestamp) else row['date_of_birth']
                dob_date = datetime.strptime(dob_str, '%d-%m-%Y').date()
                teacher_data = {
                    'teacher_name': row['teacher_name'],
                    'father_name': row['father_name'],
                    'mother_name': row['mother_name'],
                    'pan_card': row['pan_card'],
                    'aadhar_card': row['aadhar_card'],
                    'mobile_number': row['mobile_number'],
                    'subject': row['subject'],
                    'salary': row['salary'],
                    'alter_number': row['alter_number'],
                    'date_of_birth': dob_date,
                    'previous_school_name': row['previous_school_name'],
                    'transport_fees': row['transport_fees'],
                    'created_by': 'Anand'
                }
                serializer = TeacherSerializer(data=teacher_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Teachers uploaded successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class DownloadTeacherTemplateView(APIView):
    def get(self, request, *args, **kwargs):
        file_path = os.path.join(settings.MEDIA_ROOT, 'teacher', 'teacher_registeration.xlsx')
        
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="teacher_registeration.xlsx"'
            return response
        else:
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)