from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from .models import Student
from .serializers import StudentSerializer


class StudentView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    lookup_url_kwarg = "student_id"
