# from django.contrib.auth.models import User
from .serializers import StudentsRegistrationSerializer, MentorsRegistrationSerializer
from django.shortcuts import render

# Create your views here.
from .models import CustomUser

from rest_framework import generics
from rest_framework.permissions import AllowAny


class StudentsRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = StudentsRegistrationSerializer


class MentorsRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = MentorsRegistrationSerializer
