from django.shortcuts import render
from .models import TeacherDetails
from .serializers import TeacherSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TeacherDetails

# Create your views here.
class TeacherDetailsListCreateAPIView(APIView):
    def get(self, request, format=None):
        teachers = TeacherDetails.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)